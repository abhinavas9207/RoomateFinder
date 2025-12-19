
# Create your models here.
#ROOM MODEL

from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    ROLE_CHOICES=(
        ('OWNER','owner'),
        ('CUSTOMER','customer'),
        
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    def __str__(self):
        return f"{self.username}({self.role})"
    def full_name(self):
        """Returns the user's first and last name together."""
        return f"{self.first_name} {self.last_name}".strip()


class User_Profile(models.Model):
    user=models.OneToOneField(Custom_User,on_delete=models.CASCADE,related_name='Customer_Profile')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    gender=models.CharField(
        max_length=20,
        choices=[
            ('MALE', 'male'),
            ('FEMALE', 'female'),
        ]
    )
    age=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    occupation=models.CharField(
        max_length=20,
        choices=[
            ('STUDENT','student'),
            ('PFOFESSIONAL','professional'),
        ]
    )
    bio= models.TextField(null=True, blank=True)
    location=models.TextField()
    profile_image=models.ImageField(upload_to='roomimage/', blank=True, null=True)
    verified=models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)


class Owner_Profile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True)
    verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_listings = models.IntegerField(default=0)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} (Owner)"





class Room_Details(models.Model):
    owner = models.ForeignKey(Owner_Profile, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    location = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateTimeField()
    room_type = models.CharField(
        max_length=20,
        choices=[
            ('PRIVATE', 'private'),
            ('SHARED', 'shared'),
        ]
    )
    gender_preference = models.CharField(
        max_length=20,
        choices=[
            ('MALE', 'male'),
            ('FEMALE', 'female'),
        ]
    )
    image = models.ImageField(upload_to='roomimage/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


#PREFERENCE MODEL


class Preference(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="preferences")
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_location = models.TextField()
    
    # ✔ Store CSV string (not limited to single choice)
    hobbies = models.CharField(max_length=300, blank=True)

    gender_preference = models.CharField(
        max_length=20,
        choices=[
            ('MALE', 'male'),
            ('FEMALE', 'female'),
        ]
    )
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    cleanliness = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'low'),
            ('MEDIUM', 'medium'),
            ('HIGH', 'high'),
        ]
    )
    lifestyle_notes = models.TextField(blank=True, null=True)


#REVIEW MODEL


class Review(models.Model):
    user=models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name="Review")
    room=models.ForeignKey(Owner_Profile,on_delete=models.CASCADE,related_name="Review")
    rating=models.CharField(
        max_length=20,
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),

        ]
    )
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


#REPORT MODEL

class Report(models.Model):
    reason=models.TextField()
    status=models.CharField(
        max_length=20,
        choices=[
            ('PENDING','pending'),
            ('RESOLVED','resolved'),
        ]

    )
    created_at=models.DateTimeField(auto_now_add=True)





class ChatRoom(models.Model):
    participants = models.ManyToManyField(Custom_User)
    room = models.ForeignKey(Room_Details, on_delete=models.CASCADE, null=True, blank=True)  # optional

    def __str__(self):
        return f"ChatRoom {self.id}"



class ChatMessage(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)