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
    list_display = ('title', 'date', 'time', 'description')
    search_fields = ('title', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
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
