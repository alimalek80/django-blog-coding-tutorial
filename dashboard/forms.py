# dashboard/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = [
            'image', 'phone', 'city', 'country',
            'linkedin', 'github', 'website', 'x_account'
        ]
        labels = {
            'x_account': 'X (Twitter)',
            'whatsapp': 'WhatsApp',
            'telegram': 'Telegram'
        }
