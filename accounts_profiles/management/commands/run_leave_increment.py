from django.core.management.base import BaseCommand
from accounts_profiles.models import UserProfile


class Command(BaseCommand):
    help = 'Apply monthly leave increment to all active user profiles'

    def handle(self, *args, **kwargs):
        profiles = UserProfile.objects.filter(user__is_active=True)
        count = 0
        for profile in profiles:
            profile.apply_increment()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Processed {count} profiles.'))