from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.forms import ValidationError
from django.contrib.auth import get_user_model

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the signup form.
        """
        user = super().save_user(request, user, form, commit=False)
        
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = data.get('username')
        user.bio = data.get('bio', '')
        user.role = data.get('role', 'student')
        user.date_of_birth = data.get('date_of_birth')
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        
        if data.get('avatar'):
            user.avatar = data.get('avatar')
        
        if commit:
            user.save()
        return user

    def clean_email(self, email):
        """
        Validates the email address.
        """
        email = super().clean_email(email)
        return self.validate_unique_email(email)
    
    def clean_username(self, username):
        """
        Validates the username.
        """
        username = super().clean_username(username)
        return username
    
    def validate_unique_email(self, email):
        """
        Validates that the email is unique.
        """
        User = get_user_model()
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("A user is already registered with this email address.")
        return email
