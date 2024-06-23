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
    return render(request, 'index.html', {'classes': classes})

# login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, '/login.html', {'form': form})

# registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# booking
@login_required
def book_class(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    if Booking.objects.filter(user=request.user, yoga_class=yoga_class).exists():
        messages.error(request, 'You have already booked this class.')
    else:
        Booking.objects.create(user=request.user, yoga_class=yoga_class)
        messages.success(request, 'Class booked successfully!')
    return redirect('home')

# comments
@login_required
def add_comment(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, yoga_class=yoga_class, text=text)
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')