from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
     """
    Represents a user profile, containing additional information such as profile picture.
    
    Attributes:
        user (User): A one-to-one relationship with the built-in User model.
        profile_picture (ImageField): An optional field for the profile picture of the user.
    """
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

     def __str__(self):
        return self.user.username


class LiveClass(models.Model):
    """
    Represents a live class that users can book.
    
    Attributes:
        title (str): The title of the live class.
        date (date): The date when the live class will occur.
        time (time): The time when the live class will occur.
        description (str): A detailed description of the live class.
        featured_image (CloudinaryField): An optional field for the image representing the live class.
    """
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title

class Booking(models.Model):
    """
    Represents a booking of a user for a specific live class.
    
    Attributes:
        user (User): A foreign key to the user who made the booking.
        live_class (LiveClass): A foreign key to the live class that is booked.
        booked_at (datetime): The date and time when the booking was made.
    """
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


