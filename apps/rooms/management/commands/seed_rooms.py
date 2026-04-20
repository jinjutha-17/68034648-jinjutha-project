from django.core.management.base import BaseCommand
from apps.rooms.models import Room


class Command(BaseCommand):
    help = 'Seed the database with initial room data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old rooms...')
        Room.objects.all().delete()

        floor_plans = {
            1: [101, 102, 103, 104, 105, 106, 107, 108],
            2: [201, 202, 203, 204, 205, 206, 207, 208],
            3: [301, 302, 303, 304, 305, 306, 307],
            4: [401, 402, 403, 404, 405, 406, 407],
        }

        room_count = 0
        self.stdout.write('Creating rooms...')
        for floor, numbers in floor_plans.items():
            for room_number in numbers:
                Room.objects.create(
                    room_number=str(room_number),
                    floor=floor,
                    room_type='รายเดือน',
                    status='ว่าง',
                    size_sqm=28.5,
                    monthly_rent=5000.00
                )
                room_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully inserted {room_count} rooms into database.'))
