import os
import django
from datetime import datetime, date, timezone

from django.contrib.auth.hashers import make_password
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()


def execute_sql(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])


def ensure_room(room_number, floor, room_type, size_sqm, monthly_rent, status='ว่าง'):
    execute_sql(
        """
        IF NOT EXISTS (SELECT 1 FROM rooms_room WHERE room_number = %s)
        BEGIN
            INSERT INTO rooms_room
                (room_number, floor, room_type, size_sqm, monthly_rent, status, description, image, created_at)
            VALUES
                (%s, %s, %s, %s, %s, %s, '', '', %s)
        END
        """,
        [room_number, str(room_number), floor, room_type, size_sqm, monthly_rent, status, datetime.now(timezone.utc)],
    )


def ensure_user(username, email, first_name, last_name, password):
    password_hash = make_password(password)
    execute_sql(
        """
        IF NOT EXISTS (SELECT 1 FROM auth_user WHERE username = %s)
        BEGIN
            INSERT INTO auth_user
                (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES
                (%s, NULL, 0, %s, %s, %s, %s, 0, 1, %s)
        END
        """,
        [username, password_hash, username, first_name, last_name, email, datetime.now(timezone.utc)],
    )


def ensure_user_profile(username, role='Tenant'):
    execute_sql(
        """
        IF NOT EXISTS (
            SELECT 1 FROM tenants_userprofile
            WHERE user_id = (SELECT id FROM auth_user WHERE username = %s)
        )
        BEGIN
            INSERT INTO tenants_userprofile (role, user_id)
            VALUES (%s, (SELECT id FROM auth_user WHERE username = %s))
        END
        """,
        [username, role, username],
    )


def ensure_tenant(first_name, last_name, email, phone, room_number, move_in_date):
    execute_sql(
        """
        IF NOT EXISTS (SELECT 1 FROM tenants_tenant WHERE email = %s)
        BEGIN
            INSERT INTO tenants_tenant
                (first_name, last_name, email, phone, id_card, emergency_contact, emergency_phone,
                 move_in_date, move_out_date, is_active, notes, created_at, room_id)
            VALUES
                (%s, %s, %s, %s, '', '', '', %s, NULL, 1, '', %s,
                 (SELECT id FROM rooms_room WHERE room_number = %s))
        END
        """,
        [email, first_name, last_name, email, phone, move_in_date, datetime.now(timezone.utc), str(room_number)],
    )


def ensure_contract(email, room_number, start_date, end_date, monthly_rent, deposit_amount):
    execute_sql(
        """
        IF NOT EXISTS (
            SELECT 1 FROM tenants_contract
            WHERE tenant_id = (SELECT id FROM tenants_tenant WHERE email = %s)
              AND room_id = (SELECT id FROM rooms_room WHERE room_number = %s)
              AND start_date = %s
        )
        BEGIN
            INSERT INTO tenants_contract
                (tenant_id, room_id, contract_date, start_date, end_date, monthly_rent,
                 deposit_amount, is_active, document, created_at)
            VALUES
                ((SELECT id FROM tenants_tenant WHERE email = %s),
                 (SELECT id FROM rooms_room WHERE room_number = %s),
                 %s, %s, %s, %s, %s, 1, '', %s)
        END
        """,
        [email, str(room_number), start_date, email, str(room_number), datetime.now(timezone.utc), start_date, end_date, monthly_rent, deposit_amount, datetime.now(timezone.utc)],
    )


def ensure_invoice(email, room_number, invoice_date, due_date, amount, status, notes):
    execute_sql(
        """
        IF NOT EXISTS (
            SELECT 1 FROM payments_invoice
            WHERE tenant_id = (SELECT id FROM tenants_tenant WHERE email = %s)
              AND room_id = (SELECT id FROM rooms_room WHERE room_number = %s)
              AND invoice_date = %s
        )
        BEGIN
            INSERT INTO payments_invoice
                (invoice_date, due_date, amount, status, notes, created_at, room_id, tenant_id)
            VALUES
                (%s, %s, %s, %s, %s, %s,
                 (SELECT id FROM rooms_room WHERE room_number = %s),
                 (SELECT id FROM tenants_tenant WHERE email = %s))
        END
        """,
        [email, str(room_number), invoice_date, invoice_date, due_date, amount, status, notes, datetime.now(timezone.utc), str(room_number), email],
    )


def seed_sample_data():
    sample_rooms = [101, 102, 103, 104, 105]
    for room_number in sample_rooms:
        ensure_room(room_number, int(str(room_number)[0]), 'รายเดือน', 28.5, 6000.00)

    tenants = [
        {
            'username': 'nicha',
            'email': 'nicha@example.com',
            'first_name': 'Nicha',
            'last_name': 'Srisuk',
            'phone': '0812345678',
            'room_number': 101,
            'move_in_date': date(2025, 1, 5),
            'start_date': date(2025, 1, 5),
            'end_date': date(2026, 1, 4),
            'monthly_rent': 6200.00,
            'deposit_amount': 6200.00,
            'invoice_date': date(2025, 3, 1),
            'due_date': date(2025, 3, 10),
            'invoice_status': 'unpaid',
            'invoice_notes': 'Rent for March 2025',
        },
        {
            'username': 'pong',
            'email': 'pong@example.com',
            'first_name': 'Pong',
            'last_name': 'Chaiya',
            'phone': '0898765432',
            'room_number': 102,
            'move_in_date': date(2025, 2, 10),
            'start_date': date(2025, 2, 10),
            'end_date': date(2026, 2, 9),
            'monthly_rent': 6300.00,
            'deposit_amount': 6300.00,
            'invoice_date': date(2025, 4, 1),
            'due_date': date(2025, 4, 10),
            'invoice_status': 'unpaid',
            'invoice_notes': 'Rent for April 2025',
        },
    ]

    for tenant in tenants:
        ensure_user(tenant['username'], tenant['email'], tenant['first_name'], tenant['last_name'], 'tenant1234')
        ensure_user_profile(tenant['username'])
        ensure_tenant(
            tenant['first_name'],
            tenant['last_name'],
            tenant['email'],
            tenant['phone'],
            tenant['room_number'],
            tenant['move_in_date'],
        )
        ensure_contract(
            tenant['email'],
            tenant['room_number'],
            tenant['start_date'],
            tenant['end_date'],
            tenant['monthly_rent'],
            tenant['deposit_amount'],
        )
        ensure_invoice(
            tenant['email'],
            tenant['room_number'],
            tenant['invoice_date'],
            tenant['due_date'],
            tenant['monthly_rent'],
            tenant['invoice_status'],
            tenant['invoice_notes'],
        )

    print('Sample rooms and tenants created. Use username/password: nicha/tenant1234 and pong/tenant1234')


if __name__ == '__main__':
    seed_sample_data()
