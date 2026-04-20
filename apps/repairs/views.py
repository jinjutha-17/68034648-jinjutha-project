import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Repair
from .forms import RepairForm
from apps.tenants.models import Tenant


def get_user_role(user):
    if user.is_superuser or user.is_staff:
        return 'Admin'
    return getattr(getattr(user, 'profile', None), 'role', 'Tenant')


@login_required
def repair_list(request):
    user = request.user
    role = get_user_role(user)

    if role == 'Tenant':
        tenant = Tenant.objects.filter(email=user.email).first()
        repairs = Repair.objects.filter(tenant=tenant) if tenant else Repair.objects.none()
    else:
        repairs = Repair.objects.all()

    status_filter = request.GET.get('status', '')
    if status_filter:
        repairs = repairs.filter(status=status_filter)

    repairs = repairs.order_by('-created_at')

    return render(request, 'repairs/repair_list.html', {
        'repairs': repairs,
        'status_filter': status_filter,
        'role': role,
    })


@login_required
def repair_create(request):
    role = get_user_role(request.user)

    if role != 'Tenant':
        messages.error(request, 'เฉพาะผู้เช่าเท่านั้นที่สามารถแจ้งซ่อมได้')
        return redirect('repairs:list')

    tenant = Tenant.objects.filter(email=request.user.email).first()
    if not tenant:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่า')
        return redirect('tenants:tenant_home')

    if not tenant.room:
        messages.error(request, 'ผู้เช่ายังไม่ได้เลือกห้อง')
        return redirect('tenants:tenant_home')

    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.tenant = tenant
            repair.room = tenant.room
            repair.save()
            messages.success(request, 'แจ้งซ่อมเรียบร้อยแล้ว')
            return redirect('repairs:list')
    else:
        form = RepairForm()

    return render(request, 'repairs/repair_form.html', {
        'form': form,
        'title': 'แจ้งซ่อม',
        'role': role,
    })


@login_required
def repair_edit(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    role = get_user_role(request.user)

    if role == 'Tenant':
        tenant = Tenant.objects.filter(email=request.user.email).first()
        if not tenant or repair.tenant != tenant:
            messages.error(request, 'คุณไม่มีสิทธิ์แก้ไขรายการนี้')
            return redirect('repairs:list')

    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repair)
        if form.is_valid():
            updated_repair = form.save(commit=False)

            if role == 'Tenant':
                updated_repair.tenant = repair.tenant
                updated_repair.room = repair.room

            updated_repair.save()
            messages.success(request, 'อัปเดทรายการแจ้งซ่อมเรียบร้อย')
            return redirect('repairs:list')
    else:
        form = RepairForm(instance=repair)

    return render(request, 'repairs/repair_form.html', {
        'form': form,
        'title': 'แก้ไขการแจ้งซ่อม',
        'repair': repair,
        'role': role,
    })


@login_required
def repair_delete(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    role = get_user_role(request.user)

    if role == 'Tenant':
        tenant = Tenant.objects.filter(email=request.user.email).first()
        if not tenant or repair.tenant != tenant:
            messages.error(request, 'คุณไม่มีสิทธิ์ลบรายการนี้')
            return redirect('repairs:list')

    if request.method == 'POST':
        repair.delete()
        messages.success(request, 'ลบรายการแจ้งซ่อมแล้ว')
        return redirect('repairs:list')

    return render(request, 'repairs/repair_confirm_delete.html', {
        'repair': repair,
        'role': role,
    })


@login_required
@require_POST
def ajax_create(request):
    role = get_user_role(request.user)

    if role != 'Tenant':
        return JsonResponse({
            'success': False,
            'message': 'เฉพาะผู้เช่าเท่านั้นที่สามารถแจ้งซ่อมได้'
        }, status=403)

    try:
        data = json.loads(request.body)

        tenant = Tenant.objects.filter(email=request.user.email).first()
        if not tenant:
            return JsonResponse({
                'success': False,
                'message': 'ไม่พบข้อมูลผู้เช่า'
            }, status=400)

        if not tenant.room:
            return JsonResponse({
                'success': False,
                'message': 'ผู้เช่ายังไม่ได้เลือกห้อง'
            }, status=400)

        issue = data.get('issue', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        category_label = data.get('category_label', '').strip()
        priority = data.get('priority', 'medium').strip()

        if not issue:
            return JsonResponse({
                'success': False,
                'message': 'กรุณาระบุรายการที่ต้องการแจ้งซ่อม'
            }, status=400)

        Repair.objects.create(
            tenant=tenant,
            room=tenant.room,
            issue=issue,
            description=description or f'แจ้งซ่อม {category_label or category}: {issue}',
            category=category,
            category_label=category_label,
            priority=priority if priority in ['low', 'medium', 'high', 'urgent'] else 'medium',
            status='pending',
            is_seen_by_admin=False,
        )

        return JsonResponse({
            'success': True,
            'message': 'แจ้งซ่อมเรียบร้อยแล้ว'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'รูปแบบข้อมูลไม่ถูกต้อง'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)