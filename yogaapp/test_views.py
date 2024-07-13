from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from yogaapp.models import LiveClass, Booking

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

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login_view')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_login_view_post_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))  # Adjust to your actual logged-in home view

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Invalid username or password. Please try again.' for message in messages))
    
    def test_login_view_post_invalid_form(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Invalid username or password. Please try again.' for message in messages))