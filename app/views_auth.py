# views_auth.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Custom_User, Owner_Profile, User_Profile
from .forms import CustomUserForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserForm
from .models import Custom_User, User_Profile, Owner_Profile


def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please complete your profile.")

            # Auto-login after register (IMPORTANT)
            login(request, user)

            if user.role == 'OWNER':
                return redirect('owner_profile_complete')
            else:
                return redirect('create_profile')
    else:
        form = CustomUserForm()

    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            if user.role == 'OWNER':
                return redirect('owner_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')
