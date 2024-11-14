from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from .helpers import standardize_input


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
            return render(request, 'register.html')

        if password == confirm_password:
            # Create the user with first name and last name
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'income_categories': "Salary,Investment,Bonus",
            'expense_categories': "Food,Rent,Transport,Entertainment"
        }
    )

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.income_categories = standardize_input(profile.income_categories)
            profile.expense_categories = standardize_input(profile.expense_categories)
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'profile.html', context)

@login_required
def delete_user_view(request):
    if request.method == 'POST':
        # Confirm the user is deleting their own account
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to a home page or landing page after deletion

    return render(request, 'delete_user.html')
    