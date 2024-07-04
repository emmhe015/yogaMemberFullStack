from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import YogaClass, LiveClass, Booking, Comment
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from django.core.mail import send_mail


# homepage
def home(request):
    yoga_classes = YogaClass.objects.all()
    return render(request, 'index.html', {'yoga_classes': yoga_classes})

# homepage for logged in
@login_required
def home_logged_in(request):
    live_classes = LiveClass.objects.all().order_by('date', 'time')
    return render(request, 'home.html', {'live_classes': live_classes})


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
                return redirect('home_logged_in')
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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home_logged_in') 
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

# update profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})


# booking
@login_required
def booking_view(request, class_id):
    live_class = get_object_or_404(LiveClass, id=class_id)
    booking, created = Booking.objects.get_or_create(user=request.user, live_class=live_class)
    if created:
        send_mail(
            'Booking Confirmation',
            f'You have booked {live_class.title} on {live_class.date} at {live_class.time}.',
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )
        return render(request, 'booking/success.html', {'live_class': live_class})
    else:
        return render(request, 'booking/already_booked.html', {'live_class': live_class})


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
    return redirect('logout.html')