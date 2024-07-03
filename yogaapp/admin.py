from django.contrib import admin
from .models import Profile, YogaClass, Booking, Comment, Post
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')

@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'type', 'max_members')

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
    list_display = ('user', 'yoga_class', 'text', 'created_at')
