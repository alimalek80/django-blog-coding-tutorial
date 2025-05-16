from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    #private field
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    # Public profile fields
    image = models.ImageField(_('Profile Image'), upload_to='profiles/', blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    github = models.URLField(_('GitHub'), blank=True)
    website = models.URLField(_('Website'), blank=True)
    x_account = models.URLField(_('X (Twitter)'), blank=True)
    telegram = models.URLField(_('Telegram'), blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    country = models.CharField(_('Country'), blank=True, max_length=100)

    def __str__(self):
        return f"{self.user.email}'s Profile"
