from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Custom_User,
    User_Profile,
    Owner_Profile,
    Room_Details,
    Preference,
    Review,
    Report
)

# -------------------------------------------
# 🔐 USER REGISTRATION FORM
# -------------------------------------------
class CustomUserForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = ['username', 'first_name','last_name','email', 'role', 'password1', 'password2']


# -------------------------------------------
# 👤 USER PROFILE FORM
# -------------------------------------------
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
            'name', 'email', 'gender', 'age', 'phone', 'occupation',
            'bio', 'location', 'profile_image', 'verified'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'location': forms.Textarea(attrs={'rows': 2}),
        }




from django import forms
from .models import Custom_User

class OwnerUserUpdateForm(forms.ModelForm):
    class Meta:
        model = Custom_User
        fields = ['first_name', 'last_name']

# -------------------------------------------
# 🏠 OWNER PROFILE FORM
# -------------------------------------------
class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner_Profile
        fields = [
            'address', 'contact_number', 'id_proof'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


# -------------------------------------------
# 🏡 ROOM DETAILS FORM
# -------------------------------------------
class RoomDetailsForm(forms.ModelForm):
    class Meta:
        model = Room_Details
        fields = [
            'owner', 'title', 'description', 'location', 'rent',
            'available_from', 'room_type', 'gender_preference',
            'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'location': forms.Textarea(attrs={'rows': 2}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
        }


# -------------------------------------------
# 🎯 PREFERENCE FORM
# -------------------------------------------
class PreferenceForm(forms.ModelForm):
    HOBBY_CHOICES = [
        ('SINGING', 'Singing'),
        ('DRAWING', 'Drawing'),
        ('PHOTOGRAPHY', 'Photography'),
        ('GAMING', 'Gaming'),
        ('PROGRAMMING', 'Programming'),
        ('VLOGGING', 'Vlogging'),
        ('READING', 'Reading'),
        ('COOKING', 'Cooking'),
        ('DANCING', 'Dancing'),
        ('TRAVELING', 'Traveling'),
        ('LISTENING TO MUSIC', 'Listening to Music'),
    ]

    # ✅ Override hobbies as MultipleChoiceField
    hobbies = forms.MultipleChoiceField(
        choices=HOBBY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Preference
        fields = [
            'budget_min', 'budget_max', 'preferred_location',
            'hobbies', 'gender_preference', 'smoking',
            'drinking', 'pets', 'cleanliness', 'lifestyle_notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        locations = Room_Details.objects.values_list('location', flat=True).distinct()
        self.fields['preferred_location'].widget = forms.Select(
            choices=[(loc, loc) for loc in locations]
        )

        # Pre-fill hobbies from CSV string in model
        if self.instance.pk and self.instance.hobbies:
            self.initial['hobbies'] = self.instance.hobbies.split(',')

    def clean_hobbies(self):
        data = self.cleaned_data.get('hobbies')
        return ",".join(data) if data else ""



# -------------------------------------------
# ⭐ REVIEW FORM
# -------------------------------------------
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'room', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


# -------------------------------------------
# 🚨 REPORT FORM
# -------------------------------------------
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'status']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
