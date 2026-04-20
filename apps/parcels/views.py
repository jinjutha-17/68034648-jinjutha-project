from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Parcel
from .forms import ParcelForm
from apps.tenants.models import Tenant
from django.db.models import Q

@login_required
def parcel_list(request):
    user = request.user
    role = 'Client'
    if hasattr(user, 'profile'):
        role = user.profile.role

    # Client View
    if role in ['Client', 'Tenant']:
        tenant = Tenant.objects.filter(email=user.email).first()
        if not tenant or not tenant.room:
            return render(request, 'parcels/tenant_parcel_list.html', {
                'parcels': [],
                'error': 'ไม่พบข้อมูลผู้เช่าหรือห้องพักที่ผูกกับบัญชีนี้'
            })
        
        parcels = Parcel.objects.filter(room=tenant.room).order_by('-received_at')
        return render(request, 'parcels/tenant_parcel_list.html', {
            'parcels': parcels,
            'tenant': tenant
        })

    # Admin / Staff View
    # Check permissions if Staff or legacy Employee
    if role in ['Staff', 'Employee'] and not user.employee_permission.can_manage_parcels:
        messages.error(request, 'คุณไม่มีสิทธิ์เข้าถึงระบบจัดการพัสดุ')
        return redirect('dashboard')

    # Tabs filtering
    status_filter = request.GET.get('status', 'pending') # 'pending', 'received', 'all'
    search_query = request.GET.get('search', '')

    parcels = Parcel.objects.all()

    if status_filter == 'pending':
        parcels = parcels.filter(status='pending')
    elif status_filter == 'received':
        parcels = parcels.filter(status='received')
    
    if search_query:
        parcels = parcels.filter(
            Q(room__room_number__icontains=search_query) |
            Q(tracking_number__icontains=search_query) |
            Q(tenant__first_name__icontains=search_query) |
            Q(tenant__last_name__icontains=search_query)
        )

    form = ParcelForm()
    
    context = {
        'parcels': parcels,
        'status_filter': status_filter,
        'search_query': search_query,
        'form': form,
        'page_title': 'Parcel Management',
        'page_subtitle': 'ระบบจัดการพัสดุเข้า-ออก',
    }
    return render(request, 'parcels/parcel_list.html', context)

@login_required
def add_parcel(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST, request.FILES)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.created_by = request.user
            # Automatically link to the current tenant of the room
            if parcel.room.current_tenant:
                parcel.tenant = parcel.room.current_tenant
            parcel.save()
            messages.success(request, f'บันทึกพัสดุหมายเลข {parcel.tracking_number} เรียบร้อยแล้ว ระบบได้แจ้งเตือนผู้เช่าแล้ว')
            return redirect('parcel_list')
        else:
            messages.error(request, 'เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาตรวจสอบอีกครั้ง')
    return redirect('parcel_list')

@login_required
def confirm_receipt(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    
    # Security check: Tenant can only confirm their own room's parcels
    if hasattr(request.user, 'profile') and request.user.profile.role in ['Client', 'Tenant']:
        tenant = Tenant.objects.filter(email=request.user.email).first()
        if not tenant or parcel.room != tenant.room:
            messages.error(request, 'คุณไม่มีสิทธิ์ดำเนินการกับพัสดุนี้')
            return redirect('parcel_list')

    parcel.status = 'received'
    parcel.delivered_at = timezone.now()
    parcel.save()
    
    messages.success(request, 'ยืนยันการรับพัสดุเรียบร้อยแล้ว')
    return redirect('parcel_list')
