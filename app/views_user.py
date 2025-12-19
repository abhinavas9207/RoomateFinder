# views_user.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import User_Profile, Preference, Room_Details, Review
from .forms import UserProfileForm, PreferenceForm, ReviewForm

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render
from .models import Room_Details, Preference, Review, User_Profile

@login_required
def user_dashboard(request):
    # --- SEARCH FEATURE ---
    query = request.GET.get('search', '')
    if query:
        rooms = Room_Details.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        rooms = Room_Details.objects.all()

    # --- STATISTICS SECTION ---
    total_rooms = rooms.count()

    # Reviews given by current user (if any)
    rated_rooms = Review.objects.filter(user__user=request.user).count()

    # Roommate preferences created by user
    roommates_found = Preference.objects.filter(user__user=request.user).count()

    context = {
        'rooms': rooms,
        'query': query,
        'total_rooms': total_rooms,
        'rated_rooms': rated_rooms,
        'roommates_found': roommates_found,
    }
    return render(request, 'user_dashboard.html', context)


@login_required
@login_required
def user_profile(request):
    try:
        profile = User_Profile.objects.get(user=request.user)
        created = False
    except User_Profile.DoesNotExist:
        profile = None
        created = True

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'created': created})





@login_required
def create_profile(request):
    profile = getattr(request.user, 'userprofile', None)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('user_dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'create_profile.html', {'form': form})



@login_required
def user_preferences(request):
    user_profile = User_Profile.objects.get(user=request.user)

    preference = Preference.objects.filter(user=user_profile).first()

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            pref = form.save(commit=False)
            pref.user = user_profile
            pref.save()
            messages.success(request, "Preferences saved successfully!")
            return redirect('user_dashboard')
    else:
        form = PreferenceForm(instance=preference)

    return render(request, 'create_preference.html', {'form': form})



@login_required
def find_roommates(request):
    try:
        my_pref = Preference.objects.get(user__user=request.user)
        roommates = Preference.objects.filter(
            Q(preferred_location__icontains=my_pref.preferred_location),
            Q(gender_preference=my_pref.gender_preference),
            Q(cleanliness=my_pref.cleanliness)
        ).exclude(user__user=request.user)
    except Preference.DoesNotExist:
        roommates = []
    return render(request, 'find_roommates.html', {'roommates': roommates})


@login_required
def rate_room(request, room_id):
    room = get_object_or_404(Room_Details, pk=room_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = User_Profile.objects.get(user=request.user)
            review.room = room.owner
            review.save()
            messages.success(request, "Room rated successfully!")
            return redirect('user_dashboard')
    else:
        form = ReviewForm()
    return render(request, 'rate_room.html', {'form': form, 'room': room})
