from django.apps import AppConfig

class AccountsProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts_profiles'

    def ready(self):
        import accounts_profiles.models

        from accounts_profiles.scheduler import start
        start()