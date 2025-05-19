from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = [
            'image', 'full_name', 'phone', 'city', 'country',
            'birthdate', 'bio',
            'linkedin', 'github', 'website', 'x_account', 'telegram'
        ]
        labels = {
            'x_account': 'X(Twitter)',
            'image': 'Profile Image',
            'full_name': 'Full Name',
            'phone': 'Phone Number',
            'city': 'City',
            'country': 'Country',
            'birthdate': 'Birth Date',
            'bio': 'Bio',
            'linkedin': 'LinkedIn',
            'github': 'Github',
            'website': 'Website',
            'telegram': 'Telegram ID',
        }