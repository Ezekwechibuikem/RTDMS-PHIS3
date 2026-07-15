import os 
import threading
from django.apps import AppConfig

class AccountsProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts_profiles'

    def ready(self):
        # Prevents duplicate execution caused by Django's autoreload feature
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Start the background thread for the periodic task
        from accounts_profiles.scheduler import start 

        thread = threading.Thread(target=start)
        thread.daemon = True  # Ensure the thread exits when the main program does
        thread.start()