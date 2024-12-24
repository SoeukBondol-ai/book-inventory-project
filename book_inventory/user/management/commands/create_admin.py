from django.core.management.base import BaseCommand
from user.models import CustomUser

class Command(BaseCommand):
    help = 'Creates an admin user'

    def handle(self, *args, **options):
        username = input('Enter admin username: ')
        email = input('Enter admin email: ')
        password = input('Enter admin password: ')
        
        admin_user = CustomUser.objects.create_superuser(username=username, email=email, password=password, is_admin=True)
        self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully'))

