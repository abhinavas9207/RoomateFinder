# views_owner.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Owner_Profile, Room_Details , Custom_User
from .forms import RoomDetailsForm , OwnerProfileForm , OwnerUserUpdateForm

@login_required
def owner_dashboard(request):
    owner = get_object_or_404(Owner_Profile, user=request.user)
    rooms = Room_Details.objects.filter(owner=owner)
    return render(request, 'owner_dashboard.html', {'rooms': rooms})


@login_required
def add_room(request):
    owner = get_object_or_404(Owner_Profile, user=request.user)
    if request.method == 'POST':
        form = RoomDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = owner
            room.save()
            messages.success(request, "Room added successfully!")
            return redirect('owner_dashboard')
    else:
        form = RoomDetailsForm()
    return render(request, 'add_room.html', {'form': form})


@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room_Details, pk=pk)
    if request.method == 'POST':
        form = RoomDetailsForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect('owner_dashboard')
    else:
        form = RoomDetailsForm(instance=room)
    return render(request, 'edit_room.html', {'form': form})


@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room_Details, pk=pk)
    room.delete()
    messages.info(request, "Room deleted successfully.")
    return redirect('owner_dashboard')



@login_required
def owner_profile_complete(request):
    profile = getattr(request.user, 'ownerprofile', None)

    if request.method == 'POST':
        form = OwnerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Owner profile completed!")
            return redirect('owner_dashboard')
    else:
        form = OwnerProfileForm(instance=profile)

    return render(request, 'owner_profile_complete.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import Owner_Profile

def owner_profile(request):
    # Get the profile of the currently logged-in owner
    profile = get_object_or_404(Owner_Profile, user=request.user)
    
    return render(request, 'owner_profile.html', {'profile': profile})


@login_required
def edit_owner_profile(request):
    profile = get_object_or_404(Owner_Profile, user=request.user)

    if request.method == 'POST':
        user_form = OwnerUserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = OwnerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('owner_profile')

    else:
        user_form = OwnerUserUpdateForm(instance=request.user)
        profile_form = OwnerProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'edit_owner_profile.html', context)
