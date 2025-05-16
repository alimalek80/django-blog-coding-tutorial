from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Delete unverified users after 48 hours'

    def handle(self, *args, **kwargs):
        threshold_time = now() - timedelta(hours=48)
        users_to_delete = CustomUser.objects.filter(email_verified=False, date_joined__lt=threshold_time)

        for user in users_to_delete:
            self.stdout.write(f"Deleting unverified user: {user.email}")
            user.delete()

        self.stdout.write(self.style.SUCCESS('Unverified users deleted successfully.'))