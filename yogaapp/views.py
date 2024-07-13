from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LiveClass, Booking, Comment
from .forms import UserRegisterForm, ProfileUpdateForm



# homepage
def home(request):
    """
    Render the homepage.

    This view does not interact with any models or forms.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage.
    """
    
    return render(request, 'index.html')

# homepage for logged in
def home_logged_in(request):
    """
    Render the homepage for logged-in users, showing all live classes and user's booked classes.

    Models:
        - LiveClass: Retrieves all live classes.
        - Booking: Retrieves bookings for the logged-in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage for logged-in users.
    """
    live_classes = LiveClass.objects.all().order_by('date', 'time')
    user_bookings = Booking.objects.filter(user=request.user)
    booked_classes = [booking.live_class for booking in user_bookings]
    
    context = {
        'live_classes': live_classes,
        'booked_classes': booked_classes
    }
    
    return render(request, 'home.html', context)


# login
def login_view(request):
    """
    Handle user login.

    Forms:
        - AuthenticationForm: Used for authenticating users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered login page.
    """
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
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return redirect(reverse('registration/login.html', {'form': form}))
    

# registration
def register_view(request):
    """
    Handle user registration.

    Forms:
        - UserRegisterForm: Used for registering new users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered registration page.
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home_logged_in')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'register.html', {'user_form': user_form})
    
# update profile
@login_required
def update_profile(request):
    """
    Handle profile update for logged-in users.

    Forms:
        - ProfileUpdateForm: Used for updating user profiles.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered profile update page.
    """
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
def booking_view(request, class_id):
    """
    Handle booking of a live class for logged-in users.

    Models:
        - LiveClass: Retrieves the live class to be booked.
        - Booking: Creates a booking for the user.

    Args:
        request (HttpRequest): The request object.
        class_id (int): The ID of the live class to book.

    Returns:
        HttpResponse: The rendered booking success or already booked page.
    """
    live_class = get_object_or_404(LiveClass, id=class_id)
    booking, created = Booking.objects.get_or_create(user=request.user, live_class=live_class)
    if created:
        return render(request, 'booking/success.html', {'live_class': live_class})
    else:
        return render(request, 'booking/already_booked.html', {'live_class': live_class})

@login_required
def cancel_booking(request, class_id):
    """
    Handle cancellation of a booking for a live class.

    Models:
        - Booking: Retrieves and deletes the user's booking.

    Args:
        request (HttpRequest): The request object.
        class_id (int): The ID of the live class to cancel booking for.

    Returns:
        HttpResponseRedirect: Redirect to the logged-in homepage.
    """
    try:
        booking = Booking.objects.get(user=request.user, live_class_id=class_id)
        booking.delete()
    except Booking.DoesNotExist:
        pass
    return redirect('home_logged_in')


# comments
@login_required
def add_comment(request, class_id):
    """
    Handle adding a comment to a live class for logged-in users.

    Models:
        - LiveClass: Retrieves the live class to comment on.
        - Comment: Creates a comment for the live class.

    Args:
        request (HttpRequest): The request object.
        class_id (int): The ID of the live class to comment on.

    Returns:
        HttpResponseRedirect: Redirect to the logged-in homepage.
    """
    live_class = get_object_or_404(LiveClass, id=class_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, live_class=live_class, text=text)
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect(reverse('home_logged_in'))

@login_required
def delete_comment(request, comment_id):
    """
    Handle deletion of a comment for logged-in users.

    Models:
        - Comment: Retrieves and deletes the user's comment.

    Args:
        request (HttpRequest): The request object.
        comment_id (int): The ID of the comment to delete.

    Returns:
        HttpResponseRedirect: Redirect to the logged-in homepage.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('home_logged_in')

def logout_view(request):
    """
    Handle user logout.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirect to the logout page.
    """
    logout(request)
    return redirect('logout.html')