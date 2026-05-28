from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    leave_balance = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    last_incremented = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_monthly_increment(self):
        if self.user.role in ['STAFF', 'SUPERVISOR', 'HR']:
            return 2
        return 3

    def apply_increment(self):
        today = timezone.now().date()
        if self.last_incremented:
            if (self.last_incremented.year == today.year and
                    self.last_incremented.month == today.month):
                return
        self.leave_balance += self.get_monthly_increment()
        self.last_incremented = today
        self.save()

    @property
    def calculated_leave_balance(self):
        now = timezone.now()
        joined = self.user.date_joined
        months_elapsed = max(
            (now.year - joined.year) * 12 + (now.month - joined.month), 0
        )
        return months_elapsed * self.get_monthly_increment()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Balance: {self.leave_balance}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()