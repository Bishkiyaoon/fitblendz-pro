from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Fix admin user with known password'

    def handle(self, *args, **options):
        try:
            # Delete all existing admin users
            User.objects.filter(is_staff=True).delete()
            self.stdout.write(self.style.WARNING('Deleted all existing admin users'))
            
            # Create fresh admin user
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@fitblendz.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write(self.style.SUCCESS('Fresh admin user created successfully!'))
            self.stdout.write(f'Username: admin')
            self.stdout.write(f'Password: admin123')
            self.stdout.write(f'Email: {admin_user.email}')
            
            # Test the password
            test_user = authenticate(username='admin', password='admin123')
            if test_user:
                self.stdout.write(self.style.SUCCESS('Password verification successful!'))
            else:
                self.stdout.write(self.style.ERROR('Password verification failed!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            return False
