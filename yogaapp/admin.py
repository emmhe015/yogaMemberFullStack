from django.contrib import admin
from .models import Profile, YogaClass, Booking, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')

@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'type', 'max_members')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'yoga_class', 'booking_date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'yoga_class', 'text', 'created_at')
