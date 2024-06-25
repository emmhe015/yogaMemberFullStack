from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import YogaClass, Booking, Comment
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm

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
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home') 
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

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