from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class LiveClass(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')

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


