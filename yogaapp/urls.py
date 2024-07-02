from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='home_logged_in'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('booking/', views.booking_view, name='booking'),
    path('comment/<int:class_id>/', views.add_comment, name='add_comment'),
    path('summernote/', include('django_summernote.urls')),
    path('home_logged_in/', views.home_logged_in, name='home_logged_in'),
]