from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone

from apps.bookings.models import Booking
from apps.meters.models import Meter
from apps.parcels.models import Parcel
from apps.payments.models import Payment
from apps.repairs.models import Repair
from apps.rooms.models import Room
from apps.tenants.models import Tenant


@login_required
def dashboard(request):
    """Redirect users to the correct dashboard based on role."""
    user = request.user

    if user.is_superuser:
        return admin_dashboard(request)

    role = getattr(getattr(user, 'profile', None), 'role', None)

    if role == 'Admin' or user.is_staff:
        return admin_dashboard(request)
    if role in ['Staff', 'Employee']:
        return redirect('dashboard:staff_dashboard')
    if role == 'Tenant':
        return redirect('tenants:tenant_home')

    return redirect('tenants:tenant_home')


@login_required
def admin_dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='ว่าง').count()
    occupied_rooms = Room.objects.filter(status='ไม่ว่าง').count()
    maintenance_rooms = Room.objects.filter(status='ซ่อมบำรุง').count()
    occupancy_rate = round((occupied_rooms / total_rooms) * 100, 1) if total_rooms else 0

    total_tenants = Tenant.objects.filter(is_active=True).count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    overdue_payments = Payment.objects.filter(status='overdue').count()

    # ใช้ Repair จริง
    maintenance_requests = Repair.objects.filter(
        status__in=['pending', 'in_progress']
    ).count()

    recent_repairs = Repair.objects.select_related('room', 'tenant').order_by('-created_at')[:5]

    total_income = Payment.objects.filter(status='paid').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    rent_total = Payment.objects.filter(
        status='paid',
        payment_type='rent',
        due_date__year=today.year,
        due_date__month=today.month,
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    month_meters = Meter.objects.filter(
        reading_date__year=today.year,
        reading_date__month=today.month,
    ).select_related('room', 'tenant')

    water_total = sum(
        (meter.water_charge or Decimal('0.00')) for meter in month_meters
    ) or Decimal('0.00')

    electricity_total = sum(
        ((meter.reading_value or Decimal('0.00')) * Decimal('7.00')) for meter in month_meters
    ) or Decimal('0.00')

    recent_tenants = Tenant.objects.select_related('room').filter(
        is_active=True
    ).order_by('-created_at')[:8]

    rooms_by_floor = Room.objects.values('floor').annotate(
        total=Count('id'),
        available=Count('id', filter=Q(status='ว่าง')),
        occupied=Count('id', filter=Q(status='ไม่ว่าง')),
        maintenance=Count('id', filter=Q(status='ซ่อมบำรุง'))
    ).order_by('floor')

    monthly_rows = (
        Payment.objects.filter(
            status='paid',
            due_date__gte=month_start.replace(year=month_start.year - 1)
        )
        .annotate(month=TruncMonth('due_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    monthly_totals = {
        date(item['month'].year, item['month'].month, 1): float(item['total'] or 0)
        for item in monthly_rows
    }

    chart_labels = []
    chart_data = []
    comparison_data = []

    for offset in range(5, -1, -1):
        month_number = month_start.month - offset
        year = month_start.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        current_month = date(year, month_number, 1)
        value = monthly_totals.get(current_month, 0.0)

        chart_labels.append(current_month.strftime('%b'))
        chart_data.append(round(value, 2))
        comparison_data.append(round(value * 0.88, 2))

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'maintenance_rooms': maintenance_rooms,
        'occupancy_rate': occupancy_rate,
        'total_tenants': total_tenants,
        'pending_bookings': pending_bookings,
        'overdue_payments': overdue_payments,
        'maintenance_requests': maintenance_requests,
        'recent_repairs': recent_repairs,
        'recent_tenants': recent_tenants,
        'rooms_by_floor': rooms_by_floor,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'comparison_data': comparison_data,
        'total_income': total_income,
        'rent_total': rent_total,
        'water_total': water_total,
        'electricity_total': electricity_total,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def client_dashboard(request):
    """Enhanced dashboard for tenants with all UX context."""
    tenant = Tenant.objects.filter(email=request.user.email).first()

    room_number = 'N/A'
    total_due = Decimal('0.00')
    is_paid = True
    active_parcels = 0
    recent_parcels = []
    electric_meter = None
    maintenance_tasks = []

    if tenant:
        room_number = tenant.room.room_number if tenant.room else 'N/A'

        unpaid = Payment.objects.filter(
            tenant=tenant,
            status='pending'
        ).aggregate(total=Sum('amount'))['total']

        if unpaid and unpaid > 0:
            total_due = unpaid
            is_paid = False

        active_parcels = Parcel.objects.filter(
            tenant=tenant,
            status='pending'
        ).count()

        recent_parcels = Parcel.objects.filter(
            tenant=tenant
        ).order_by('-received_at')[:5]

        meters = Meter.objects.filter(tenant=tenant).order_by('-reading_date')[:2]
        if meters:
            electric_meter = meters[0]

        # ใช้ Repair จริง
        maintenance_tasks = Repair.objects.filter(
            tenant=tenant
        ).order_by('-created_at')[:3]

    context = {
        'tenant': tenant,
        'room_number': room_number,
        'total_due': total_due,
        'is_paid': is_paid,
        'active_parcels_count': active_parcels,
        'recent_parcels': recent_parcels,
        'maintenance_tasks': maintenance_tasks,
        'water_units': 4.2,
        'electric_units': 182,
        'prev_water': 1241.0,
        'curr_water': 1245.2,
        'prev_elec': 8560,
        'curr_elec': 8742,
        'electric_meter': electric_meter,
    }
    return render(request, 'dashboard/tenant_dashboard.html', context)


@login_required
def staff_dashboard(request):
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(status='ไม่ว่าง').count()
    pending_bookings = Booking.objects.filter(status='pending').count()

    # ใช้ Repair จริง
    maintenance_requests = Repair.objects.filter(
        status__in=['pending', 'in_progress']
    ).count()

    recent_repairs = Repair.objects.select_related('room', 'tenant').order_by('-created_at')[:5]

    context = {
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'pending_bookings': pending_bookings,
        'maintenance_requests': maintenance_requests,
        'recent_repairs': recent_repairs,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)


@login_required
def staff_management(request):
    """Staff management page showing staff list and statistics"""
    from django.contrib.auth.models import User

    employees = User.objects.filter(
        profile__role__in=['Staff', 'Employee', 'Admin']
    ).select_related('profile', 'employee_permission').order_by('-date_joined')

    total_staff = employees.count()

    context = {
        'employees': employees,
        'total_staff': total_staff,
        'page_title': 'จัดการพนักงาน',
        'page_subtitle': 'ข้อมูลพนักงานและสิทธิ์การใช้งาน',
    }
    return render(request, 'dashboard/staff_list.html', context)