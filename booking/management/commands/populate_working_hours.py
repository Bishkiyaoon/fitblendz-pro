from django.core.management.base import BaseCommand
from booking.models import WorkingHours
from datetime import time

class Command(BaseCommand):
    help = 'Populate working hours in the database'

    def handle(self, *args, **options):
        working_hours_data = [
            {
                'day': 0,  # Monday
                'is_open': True,
                'open_time': time(9, 0),  # 9:00 AM
                'close_time': time(20, 0),  # 8:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 1,  # Tuesday
                'is_open': True,
                'open_time': time(9, 0),  # 9:00 AM
                'close_time': time(20, 0),  # 8:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 2,  # Wednesday
                'is_open': True,
                'open_time': time(9, 0),  # 9:00 AM
                'close_time': time(20, 0),  # 8:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 3,  # Thursday
                'is_open': True,
                'open_time': time(9, 0),  # 9:00 AM
                'close_time': time(20, 0),  # 8:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 4,  # Friday
                'is_open': True,
                'open_time': time(9, 0),  # 9:00 AM
                'close_time': time(20, 0),  # 8:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 5,  # Saturday
                'is_open': True,
                'open_time': time(10, 0),  # 10:00 AM
                'close_time': time(21, 0),  # 9:00 PM
                'break_start': None,
                'break_end': None
            },
            {
                'day': 6,  # Sunday
                'is_open': False,  # Closed on Sunday
                'open_time': None,
                'close_time': None,
                'break_start': None,
                'break_end': None
            }
        ]

        for wh_data in working_hours_data:
            working_hours, created = WorkingHours.objects.get_or_create(
                day=wh_data['day'],
                defaults=wh_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created working hours for day {wh_data["day"]}')
                )
            else:
                # Update existing working hours
                for key, value in wh_data.items():
                    setattr(working_hours, key, value)
                working_hours.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated working hours for day {wh_data["day"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated working hours!')
        )
