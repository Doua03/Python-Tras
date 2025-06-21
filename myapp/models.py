from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from jsonschema import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from jsonschema import ValidationError

class UserRegistrationManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        # Ensure that only users can register themselves
        if 'role' in extra_fields:
            role = extra_fields['role']
            
            # Check if the role is valid
            if role not in ['user', 'admin', 'doctor']:
                raise ValueError('Invalid role assigned.')

        # Normalize the email and set password
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserRegistration(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')

    objects = UserRegistrationManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# New Model for Doctor Details
class DoctorDetails(models.Model):
    user = models.OneToOneField(UserRegistration, on_delete=models.CASCADE, related_name='doctor_details')
    doctor_name = models.CharField(max_length=255,default="Unknown")
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    clinic_address = models.TextField()
    qualifications = models.TextField()
    experience_years = models.IntegerField()
    available_days = models.CharField(
    max_length=50,
    null=True,
    blank=True,
    help_text="Comma-separated list of available days (e.g., 'Monday, Tuesday, Friday')"
    )
    start_time = models.TimeField(  null=True,
    blank=True,help_text="Start time of availability (e.g., 09:00 AM)")
    end_time = models.TimeField(  null=True,
    blank=True,help_text="End time of availability (e.g., 05:00 PM)")

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"
    def clean(self):
        super().clean()
        if self.available_days:
            days = [day.strip() for day in self.available_days.split(',')]
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days:
                if day not in valid_days:
                    raise ValidationError({'available_days': f"'{day}' is not a valid day."})
                
    def get_available_days(self):
        if self.available_days:
            return [day.strip() for day in self.available_days.split(',')]
        return []
    
    from django.db import models
from django.contrib.auth import get_user_model

class Consultation(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey('DoctorDetails', on_delete=models.CASCADE, related_name='consultations')
    consultation_type = models.CharField(max_length=7, choices=CONSULTATION_TYPE_CHOICES)
    consultation_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Consultation with {self.doctor.user.username} on {self.consultation_time.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ['consultation_time']
        constraints = [
            models.UniqueConstraint(fields=['user', 'doctor', 'consultation_time'], name='unique_consultation')
        ]
    

DIFFICULTY_CHOICES = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]

class Word(models.Model):
    word = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')

    def __str__(self):
        return self.word
    
class Story(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='stories/pdfs/')
    audio_files = models.JSONField(default=list, null=True, blank=True)  # Stores audio file paths for each page
    questions = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return self.title
