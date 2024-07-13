from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from yogaapp.models import LiveClass, Booking, Comment
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

class BookingViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a test class
        self.live_class = LiveClass.objects.create(
            title='Yoga Class',
            description='A relaxing yoga class',
            date='2023-01-01',
            time='10:00:00'
        )
        
        # Initialize the client
        self.client = Client()

    def test_booking_view_first_time(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')

        # Make a booking request
        response = self.client.get(reverse('booking', args=[self.live_class.id]))

        # Check that the booking was created
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/success.html')
        self.assertTrue(Booking.objects.filter(user=self.user, live_class=self.live_class).exists())

    def test_booking_view_already_booked(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')

        # Create a booking beforehand
        Booking.objects.create(user=self.user, live_class=self.live_class)

        # Make a booking request
        response = self.client.get(reverse('booking', args=[self.live_class.id]))

        # Check that the booking already exists
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/already_booked.html')
        self.assertEqual(Booking.objects.filter(user=self.user, live_class=self.live_class).count(), 1)

class CancelBookingViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a test class
        self.live_class = LiveClass.objects.create(
            title='Yoga Class',
            description='A relaxing yoga class',
            date='2023-01-01',
            time='10:00:00'
        )
        
        # Create a booking for the user
        self.booking = Booking.objects.create(user=self.user, live_class=self.live_class)
        
        # Initialize the client
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_cancel_booking_existing(self):
        # Make a cancel booking request
        response = self.client.get(reverse('cancel_booking', args=[self.live_class.id]))

        # Check that the booking was deleted and the user is redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertFalse(Booking.objects.filter(user=self.user, live_class=self.live_class).exists())

    def test_cancel_booking_non_existing(self):
        # Cancel an already canceled booking
        self.booking.delete()

        # Make a cancel booking request
        response = self.client.get(reverse('cancel_booking', args=[self.live_class.id]))

        # Check that the user is redirected even if the booking doesn't exist
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))

class AddCommentViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a test class
        self.live_class = LiveClass.objects.create(
            title='Yoga Class',
            description='A relaxing yoga class',
            date='2023-01-01',
            time='10:00:00'
        )
        
        # Initialize the client
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_add_comment_valid(self):
        # Make a valid comment request
        response = self.client.post(reverse('add_comment', args=[self.live_class.id]), {'text': 'Great class!'})

        # Check that the comment was created and success message is shown
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertTrue(Comment.objects.filter(user=self.user, live_class=self.live_class, text='Great class!').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Comment added successfully!')

    def test_add_comment_empty_text(self):
        # Make an empty comment request
        response = self.client.post(reverse('add_comment', args=[self.live_class.id]), {'text': ''})

        # Check that no comment was created and error message is shown
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertFalse(Comment.objects.filter(user=self.user, live_class=self.live_class).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Comment cannot be empty.')

class DeleteCommentViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create another test user
        self.other_user = User.objects.create_user(username='otheruser', password='password456')
        
        # Create a test class
        self.live_class = LiveClass.objects.create(
            title='Yoga Class',
            description='A relaxing yoga class',
            date='2023-01-01',
            time='10:00:00'
        )
        
        # Create a test comment by the test user
        self.comment = Comment.objects.create(
            user=self.user,
            live_class=self.live_class,
            text='This is a test comment'
        )
        
        # Initialize the client
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_delete_comment_by_owner(self):
        # Make a request to delete the comment by the owner
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))

        # Check that the comment was deleted and success message is shown
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Comment deleted successfully!')

    def test_delete_comment_by_non_owner(self):
        # Login as the other user
        self.client.login(username='otheruser', password='password456')

        # Make a request to delete the comment by a non-owner
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))

        # Check that the comment was not deleted and error message is shown
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_logged_in'))
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have permission to delete this comment.')

class LogoutViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Initialize the client
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_logout_view(self):
        # Make a GET request to the logout view
        response = self.client.get(reverse('logout'))

        # Check that the user is logged out and redirected to the correct page
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('logout.html'))