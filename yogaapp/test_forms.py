from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegisterForm

class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        """
        Test that a valid form with all required fields filled correctly
        will be valid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_missing_first_name(self):
        """
        Test that a form missing the first name will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': '',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_email_already_in_use(self):
        """
        Test that a form with an email that is already in use will be invalid.
        """
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='StrongPassword123!')
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        """
        Test that a form with mismatched passwords will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'DifferentPassword123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
