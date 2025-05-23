from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def user_profile_image_path(instance, filename):
    # Always save as user_{id}.jpg
    ext = filename.split('.')[-1]
    return f"profiles/user_{instance.user.id}_profile.{ext}"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Use fallback image as default
    image = models.ImageField(
        _('Profile Image'),
        upload_to=user_profile_image_path,
        blank=True,
        default='profiles/fallback-profile-image.jpg'
    )

    #private field
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    # Public profile fields
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    github = models.URLField(_('GitHub'), blank=True)
    website = models.URLField(_('Website'), blank=True)
    x_account = models.URLField(_('X (Twitter)'), blank=True)
    telegram = models.CharField(_('Telegram'), max_length=50, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    country = models.CharField(_('Country'), blank=True, max_length=100)

    full_name = models.CharField(_('Full Name'), max_length=150, blank=True)
    birthdate = models.DateField(_('Birthdate'), max_length=100, blank=True, null=True)
    bio = models.TextField(_('Bio'), blank=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
