from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Profile, Booking, Comment, LiveClass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface options for Profile model.

    List Display:
        - user: The user associated with the profile.
        - profile_picture: The profile picture of the user.
    """
    list_display = ('user', 'profile_picture')
    
@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    """
    Admin interface options for LiveClass model.

    List Display:
        - title: The title of the live class.
        - date: The date of the live class.
        - time: The time of the live class.
        - description: The description of the live class.

    Search Fields:
        - title: The title of the live class.
        - description: The description of the live class.
    """
    list_display = ('title', 'date', 'time', 'description')
    search_fields = ('title', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface options for Booking model.

    List Display:
        - user: The user who made the booking.
        - get_live_class: The title of the live class.
        - get_booking_date: The date and time when the booking was made.

    Methods:
        - get_live_class: Returns the title of the live class associated with the booking.
        - get_booking_date: Returns the date and time when the booking was made.
    """
    list_display = ('user', 'get_live_class', 'get_booking_date')

    def get_live_class(self, obj):
        return obj.live_class.title
    get_live_class.short_description = 'Live Class'

    def get_booking_date(self, obj):
        return obj.booked_at
    get_booking_date.short_description = 'Booking Date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'live_class', 'text', 'created_at')
