from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class YogaClass(models.Model):
    HATHA = 'Hatha'
    VINYASA = 'Vinyasa'
    ASHTANGA = 'Ashtanga'
    BEGINNERS = 'Beginners'
    
    CLASS_TYPES = [
        (HATHA, 'Hatha'),
        (VINYASA, 'Vinyasa'),
        (ASHTANGA, 'Ashtanga'),
        (BEGINNERS, 'Beginners'),
    ]

    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    description = models.TextField()
    type = models.CharField(max_length=20, choices=CLASS_TYPES)
    max_members = models.IntegerField(default=20)
    image = models.ImageField(upload_to='class_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.type}'

class LiveClass(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.live_class.title}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.live_class}'

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
