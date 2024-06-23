from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import YogaClass, Booking, Comment
from django.contrib import messages

# homepage
def home(request):
    classes = YogaClass.objects.all()
    return render(request, 'yogaapp/index.html', {'classes': classes})
    