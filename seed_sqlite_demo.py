from datetime import date, timedelta

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_project.settings")
django.setup()

from apps.bookings.models import Booking
from apps.payments.models import Payment
from apps.rooms.models import Room
from apps.tenants.models import Tenant


def run():
    rooms_data = [("101", 1), ("102", 1), ("201", 2), ("202", 2), ("301", 3), ("302", 3)]
    for room_number, floor in rooms_data:
        Room.objects.get_or_create(
            room_number=room_number,
            defaults={
                "floor": floor,
                "room_type": "รายเดือน",
                "size_sqm": 28.5,
                "monthly_rent": 6000.00,
                "elec_rate": 7.00,
                "water_rate": 18.00,
                "status": "ว่าง",
                "description": "",
            },
        )

    tenants_data = [
        ("Somchai", "Jaidee", "somchai@example.com", "0890000001", "101"),
        ("Suda", "Dee", "suda@example.com", "0890000002", "201"),
        ("Anan", "Meechai", "anan@example.com", "0890000003", "301"),
    ]
    for first_name, last_name, email, phone, room_number in tenants_data:
        room = Room.objects.get(room_number=room_number)
        tenant, _ = Tenant.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "room": room,
                "is_active": True,
                "move_in_date": date.today() - timedelta(days=30),
            },
        )
        if tenant.room_id != room.id:
            tenant.room = room
            tenant.is_active = True
            tenant.save(update_fields=["room", "is_active"])
        if room.status != "ไม่ว่าง":
            room.status = "ไม่ว่าง"
            room.save(update_fields=["status"])

    Booking.objects.get_or_create(
        room=Room.objects.get(room_number="102"),
        full_name="Demo Booking",
        email="guest@example.com",
        phone="0891111111",
        check_in_date=date.today() + timedelta(days=3),
        check_out_date=date.today() + timedelta(days=33),
        defaults={"status": "pending", "notes": "seed"},
    )

    for email in ["somchai@example.com", "suda@example.com", "anan@example.com"]:
        tenant = Tenant.objects.get(email=email)
        Payment.objects.get_or_create(
            tenant=tenant,
            room=tenant.room,
            payment_type="rent",
            amount=tenant.room.monthly_rent,
            due_date=date.today().replace(day=28),
            defaults={"status": "pending", "notes": "seed rent"},
        )

    print("rooms=", Room.objects.count())
    print("tenants=", Tenant.objects.count())
    print("bookings=", Booking.objects.count())
    print("payments=", Payment.objects.count())


if __name__ == "__main__":
    run()
