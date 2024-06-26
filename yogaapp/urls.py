from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('book/<int:class_id>/', views.book_class, name='book_class'),
    path('comment/<int:class_id>/', views.add_comment, name='add_comment'),
    path('summernote/', include('django_summernote.urls')),
]