from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import LiveClass, Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user with additional required fields.

    This form extends the built-in UserCreationForm to include additional
    fields for email, first name, and last name.

    Fields:
        - username: The user's username.
        - first_name: The user's first name (required).
        - last_name: The user's last name (required).
        - email: The user's email address (required).
        - password1: The user's password.
        - password2: Password confirmation.

    Meta:
        model: The User model from django.contrib.auth.models.
        fields: The fields to include in the form.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form allows users to update their first name, last name, email,
    and password. Password fields are optional and include validation.

    Fields:
        - first_name: The user's first name.
        - last_name: The user's last name.
        - email: The user's email address.
        - password: The user's new password (optional).
        - password_confirmation: Confirmation of the new password (optional).

    Meta:
        model: The User model from django.contrib.auth.models.
        fields: The fields to include in the form.

    Methods:
        clean_email: Validates the email to ensure it is not already in use.
        clean: Validates that the passwords match and validates the password strength.
    """
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirmation']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")
        
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                self.add_error('password', e)
        
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user