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
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_first_name(self):
        """
        Test that a form missing the first name will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': '',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_missing_last_name(self):
        """
        Test that a form missing the last name will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': '',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_missing_email(self):
        """
        Test that a form missing the email will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': '',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_passwords_do_not_match(self):
        """
        Test that a form where passwords do not match will be invalid.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'differentpassword'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_duplicate_email(self):
        """
        Test that a form with a duplicate email address will be invalid.
        """
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='password123')
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
