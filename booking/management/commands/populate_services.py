from django.core.management.base import BaseCommand
from booking.models import Service

class Command(BaseCommand):
    help = 'Populate services in the database'

    def handle(self, *args, **options):
        services_data = [
            {
                'name': 'Haircut',
                'description': 'Professional haircut with styling',
                'duration': 30,
                'price': 500.00,
                'is_active': True
            },
            {
                'name': 'Beard Trim',
                'description': 'Precise beard trimming and shaping',
                'duration': 20,
                'price': 300.00,
                'is_active': True
            },
            {
                'name': 'Hair & Beard',
                'description': 'Complete hair and beard service',
                'duration': 45,
                'price': 700.00,
                'is_active': True
            },
            {
                'name': 'Shave',
                'description': 'Traditional wet shave',
                'duration': 25,
                'price': 250.00,
                'is_active': True
            },
            {
                'name': 'Other',
                'description': 'Custom service as requested',
                'duration': 30,
                'price': 400.00,
                'is_active': True
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated services!')
        )
