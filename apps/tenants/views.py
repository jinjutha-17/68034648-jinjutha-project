from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator

from .models import Tenant, Contract
from .forms import TenantForm

from apps.parcels.models import Parcel
from apps.payments.models import Payment
from apps.repairs.models import Repair
from apps.meters.models import Meter


@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()
    active_filter = request.GET.get('active', '')

    if active_filter == 'yes':
        tenants = tenants.filter(is_active=True)
    elif active_filter == 'no':
        tenants = tenants.filter(is_active=False)

    paginator = Paginator(tenants, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tenants/tenant_list.html', {
        'page_obj': page_obj,
        'active_filter': active_filter
    })


@login_required
def tenant_detail(request, pk):
    if not request.user.is_staff:
        return redirect('tenants:tenant_home')

    tenant = get_object_or_404(Tenant, pk=pk)
    payments = tenant.payments.order_by('-due_date')[:10]
    contracts = tenant.contracts.order_by('-created_at')

    return render(request, 'tenants/tenant_detail.html', {
        'tenant': tenant,
        'payments': payments,
        'contracts': contracts,
    })


@login_required
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save()

            if tenant.room:
                tenant.room.status = 'ไม่ว่าง'
                tenant.room.save()

            messages.success(request, 'เพิ่มผู้เช่าสำเร็จ')
            return redirect('tenants:list')
    else:
        form = TenantForm()

    return render(request, 'tenants/tenant_form.html', {
        'form': form,
        'title': 'เพิ่มผู้เช่า'
    })


@login_required
def tenant_edit(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    old_room = tenant.room

    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            tenant = form.save()
            new_room = tenant.room

            if old_room and old_room != new_room:
                old_room.status = 'ว่าง'
                old_room.save()

            if new_room:
                new_room.status = 'ไม่ว่าง'
                new_room.save()

            messages.success(request, 'อัพเดทผู้เช่าสำเร็จ')
            return redirect('tenants:list')
    else:
        form = TenantForm(instance=tenant)

    return render(request, 'tenants/tenant_form.html', {
        'form': form,
        'title': 'แก้ไขผู้เช่า'
    })


@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)

    if request.method == 'POST':
        if tenant.room:
            tenant.room.status = 'ว่าง'
            tenant.room.save()

        tenant.delete()
        messages.success(request, 'ลบผู้เช่าสำเร็จ')
        return redirect('tenants:list')

    return render(request, 'tenants/tenant_confirm_delete.html', {
        'tenant': tenant
    })


@login_required
def tenant_home(request):
    tenant = Tenant.objects.filter(email=request.user.email).first()

    if not tenant:
        return render(request, 'tenants/tenant_home.html', {
            'error': 'ไม่พบข้อมูลผู้เช่าสำหรับบัญชีของคุณ'
        })

    room_number = tenant.room.room_number if tenant.room else 'N/A'

    # ยอดค้างชำระรวม
    unpaid_total = Payment.objects.filter(
        tenant=tenant,
        status__in=['pending', 'overdue']
    ).aggregate(total=Sum('amount'))['total'] or 0

    # payment ล่าสุดที่ยังค้าง สำหรับ popup แจ้งชำระเงิน
    latest_payment = Payment.objects.filter(
        tenant=tenant,
        status__in=['pending', 'overdue']
    ).order_by('due_date', 'id').first()

    # พัสดุ
    active_parcels = Parcel.objects.filter(
        tenant=tenant,
        status='pending'
    ).count()

    recent_parcels = Parcel.objects.filter(
        tenant=tenant
    ).order_by('-received_at')[:5]

    # แจ้งซ่อม
    maintenance_tasks = Repair.objects.filter(
        tenant=tenant
    ).order_by('-created_at')[:3]

    # มิเตอร์
    meters = Meter.objects.filter(
        tenant=tenant
    ).order_by('-reading_date')[:2]

    prev_water = 0
    curr_water = 0
    water_units = 0
    prev_elec = 0
    curr_elec = 0
    electric_units = 0

    if meters:
        latest = meters[0]
        curr_elec = latest.reading_value or 0
        curr_water = latest.water_charge or 0

        if len(meters) > 1:
            prev = meters[1]
            prev_elec = prev.reading_value or 0
            prev_water = prev.water_charge or 0

        electric_units = curr_elec - prev_elec
        water_units = curr_water - prev_water

    context = {
        'tenant': tenant,
        'full_name': tenant.full_name,
        'room_number': room_number,
        'latest_invoice': unpaid_total,
        'total_due': unpaid_total,
        'latest_payment_id': latest_payment.id if latest_payment else None,
        'active_parcels_count': active_parcels,
        'pending_parcels': active_parcels,
        'recent_parcels': recent_parcels,
        'maintenance_tasks': maintenance_tasks,
        'prev_water': prev_water,
        'curr_water': curr_water,
        'water_units': water_units,
        'prev_elec': prev_elec,
        'curr_elec': curr_elec,
        'electric_units': electric_units,
    }

    return render(request, 'tenants/tenant_home.html', context)


@login_required
def my_profile(request):
    tenant = get_object_or_404(Tenant, email=request.user.email)

    return render(request, 'tenants/tenant_detail.html', {
        'tenant': tenant
    })


@login_required
def choose_room(request):
    tenant = Tenant.objects.filter(email=request.user.email).first()
    if not tenant:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่า กรุณาติดต่อเจ้าหน้าที่')
        return redirect('tenants:tenant_home')

    from apps.rooms.models import Room

    selected_floor = request.GET.get('floor', '')
    rooms = Room.objects.filter(status='ว่าง')

    if selected_floor:
        rooms = rooms.filter(floor=selected_floor)

    floors = Room.objects.values_list('floor', flat=True).distinct().order_by('floor')

    return render(request, 'tenants/choose_room.html', {
        'rooms': rooms,
        'floors': floors,
        'selected_floor': selected_floor,
        'current_room': tenant.room,
    })


@login_required
def select_room(request, pk):
    if request.method != 'POST':
        return redirect('tenants:choose_room')

    tenant = Tenant.objects.filter(email=request.user.email).first()
    if not tenant:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่า')
        return redirect('tenants:tenant_home')

    from apps.rooms.models import Room
    new_room = get_object_or_404(Room, pk=pk, status='ว่าง')

    if tenant.room and tenant.room != new_room:
        tenant.room.status = 'ว่าง'
        tenant.room.save()

    new_room.status = 'ไม่ว่าง'
    new_room.save()

    tenant.room = new_room
    tenant.save()

    messages.success(request, f'เลือกห้อง {new_room.room_number} สำเร็จ!')
    return redirect('tenants:tenant_home')