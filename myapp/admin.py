from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserRegistration, DoctorDetails, Word
from django import forms
from django import forms
from django.core.exceptions import ValidationError
from .models import UserRegistration, DoctorDetails

class DoctorDetailsAdminForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Enter the username for the doctor")
    email = forms.EmailField(help_text="Enter the email for the doctor")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Set a password for the doctor")

    class Meta:
        model = DoctorDetails
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserRegistration.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserRegistration.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        # Extract user-related data
        username = self.cleaned_data.pop('username', None)
        email = self.cleaned_data.pop('email', None)
        password = self.cleaned_data.pop('password', None)

        # Create a UserRegistration instance
        if username and email and password:
            user = UserRegistration.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='doctor'  # Explicitly set the role to 'doctor'
            )
            # Link the user to the DoctorDetails instance
            self.instance.user = user

        return super().save(commit=commit)
    
@admin.register(DoctorDetails)
class DoctorDetailsAdmin(admin.ModelAdmin):
    form = DoctorDetailsAdminForm
    list_display = ('user', 'specialization', 'contact_number', 'available_days', 'start_time', 'end_time')
    search_fields = ('user__username', 'specialization', 'contact_number')
    list_filter = ('specialization', 'available_days')  # Add filters for easier navigation
    readonly_fields = ('user',)  # Prevent editing of the user field

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserRegistration

class UserRegistrationAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

# Register the UserRegistration model with the custom admin
admin.site.register(UserRegistration, UserRegistrationAdmin)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word',)
