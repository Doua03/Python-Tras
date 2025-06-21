from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import DoctorDetails, Story, UserRegistration
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
    )

    class Meta:
        model = UserRegistration
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserRegistration.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError("Password is too weak. Ensure it's at least 8 characters, includes a number, etc.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'user'  # Explicitly set the role to 'user'
        if commit:
            user.save()
        return user
    
from django import forms
from .models import UserRegistration

class AdminRegistrationForm(forms.ModelForm):
    department = forms.CharField(max_length=255, label="Department")

    class Meta:
        model = UserRegistration
        fields = ['username', 'email', 'department']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserRegistration.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'  # Explicitly set the role to 'admin'
        if commit:
            user.save()
        return user
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class AddDoctorForm(forms.Form):
    doctor_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    specialization = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    clinic_address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    qualifications = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    experience_years = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    available_days = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M', attrs={
        'type': 'time',
        'class': 'form-control',
        'placeholder': 'HH:MM',
    }))
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M', attrs={
        'type': 'time',
        'class': 'form-control',
        'placeholder': 'HH:MM',
    }))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    
from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['consultation_type', 'consultation_time']

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'pdf', 'audio_files', 'questions']

    questions = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'JSON format of questions'}))
