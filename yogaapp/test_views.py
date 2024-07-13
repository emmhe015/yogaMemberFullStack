from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from yogaapp.models import LiveClass, Booking
from .forms import ProfileUpdateForm

class HomeViewTest(TestCase):
    def test_home_view(self):
        """
        Test that the home view renders the correct template and returns a 200 status code.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class HomeLoggedInViewTest(TestCase):
    def setUp(self):
        """
        Set up test data.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.live_class1 = LiveClass.objects.create(title='Yoga Class 1', date='2024-07-10', time='10:00:00', description='Description 1')
        self.live_class2 = LiveClass.objects.create(title='Yoga Class 2', date='2024-07-11', time='11:00:00', description='Description 2')
        Booking.objects.create(user=self.user, live_class=self.live_class1)

    def test_home_logged_in_view(self):
        """
        Test that the home_logged_in view renders correctly for a logged-in user.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home_logged_in'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('live_classes', response.context)
        self.assertIn('booked_classes', response.context)
        
        live_classes = response.context['live_classes']
        booked_classes = response.context['booked_classes']

        self.assertEqual(list(live_classes), [self.live_class1, self.live_class2])
        self.assertEqual(list(booked_classes), [self.live_class1])

User = get_user_model()

class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser2',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='testuser2').exists())
        messages = list(get_messages(response.wsgi_request))
        
        self.assertTrue(any("password2: The two password fields didn’t match." in message.message for message in messages))

    def test_register_view_post_invalid(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': '',
            'last_name': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())
        messages = list(get_messages(response.wsgi_request))
        
        self.assertTrue(any("username: This field is required." in message.message for message in messages))
        self.assertTrue(any("first_name: This field is required." in message.message for message in messages))
        self.assertTrue(any("last_name: This field is required." in message.message for message in messages))

class UpdateProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.client.login(username='testuser', password='testpassword123')
        self.update_profile_url = reverse('update_profile')

    def test_update_profile_view_get(self):
        response = self.client.get(self.update_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')

    def test_update_profile_view_post_valid(self):
        response = self.client.post(self.update_profile_url, {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'password': '',
            'password_confirmation': ''
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')
        self.assertEqual(self.user.email, 'newemail@example.com')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your profile was successfully updated!" in message.message for message in messages))

    def test_update_profile_view_post_password_update(self):
        response = self.client.post(self.update_profile_url, {
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'email': 'testuser@example.com',
            'password': 'newpassword123',
            'password_confirmation': 'newpassword123'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_update_profile_view_post_invalid(self):
        response = self.client.post(self.update_profile_url, {
            'first_name': '',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'password': '',
            'password_confirmation': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("first_name: This field is required." in message.message for message in messages))