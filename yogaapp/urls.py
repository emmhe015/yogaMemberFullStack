from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:class_id>/', views.book_class, name='book_class'),
    path('comment/<int:class_id>/', views.add_comment, name='add_comment'),
]