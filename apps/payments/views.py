from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone

from .models import Payment, Meter, Invoice, Maintenance
from .forms import PaymentForm, MeterForm, InvoiceForm, MaintenanceForm
from apps.tenants.models import Tenant


# ==========================================
# 1. Payment Views
# ==========================================
@login_required
def payment_list(request):
    payments = Payment.objects.select_related('tenant', 'room').order_by('-due_date', '-id')

    status_filter = request.GET.get('status', '')
    if status_filter:
        payments = payments.filter(status=status_filter)

    paid_total = Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    pending_total = Payment.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'payments/payment_list.html', {
        'payments': payments,
        'status_filter': status_filter,
        'paid_total': paid_total,
        'pending_total': pending_total
    })


@login_required
def payment_approve(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'คุณไม่มีสิทธิ์ในการดำเนินการนี้')
        return redirect('payments:list')

    payment = get_object_or_404(Payment, pk=pk)

    if payment.status != 'paid':
        payment.status = 'paid'
        payment.paid_date = timezone.now().date()
        payment.save()
        messages.success(request, f'อนุมัติรายการชำระเงินของห้อง {payment.room.room_number} เรียบร้อยแล้ว')
    else:
        messages.warning(request, 'รายการนี้ได้รับการตรวจสอบแล้ว')

    return redirect('payments:list')


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payments/payment_detail.html', {'payment': payment})


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มรายการชำระเงินเรียบร้อย')
            return redirect('payments:list')
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'title': 'Add Payment'
    })


@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขข้อมูลการชำระเงินเรียบร้อย')
            return redirect('payments:list')
    else:
        form = PaymentForm(instance=payment)

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'title': 'Edit Payment'
    })


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'ลบรายการชำระเงินเรียบร้อย')
        return redirect('payments:list')

    return render(request, 'payments/payment_confirm_delete.html', {
        'payment': payment
    })


# ==========================================
# 1.1 Tenant Payment Views
# ==========================================
@login_required
def tenant_payment_list(request):
    tenant = Tenant.objects.filter(email=request.user.email).first()

    if not tenant:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่า')
        return redirect('tenants:tenant_home')

    payments = Payment.objects.filter(tenant=tenant).order_by('-due_date', '-id')

    return render(request, 'payments/tenant_payment_list.html', {
        'tenant': tenant,
        'payments': payments,
    })


@login_required
def tenant_payment_create(request):
    tenant = Tenant.objects.filter(email=request.user.email).first()

    if not tenant:
        messages.error(request, 'ไม่พบข้อมูลผู้เช่า')
        return redirect('tenants:tenant_home')

    payment = Payment.objects.filter(
        tenant=tenant,
        status__in=['pending', 'overdue']
    ).order_by('due_date', 'id').first()

    if not payment:
        messages.info(request, 'ไม่มีรายการค้างชำระ')
        return redirect('tenants:tenant_home')

    return render(request, 'payments/tenant_payment_create.html', {
        'tenant': tenant,
        'payment': payment,
    })


@login_required
def tenant_payment_submit(request, pk):
    tenant = Tenant.objects.filter(email=request.user.email).first()
    payment = get_object_or_404(Payment, pk=pk)

    if not tenant or payment.tenant != tenant:
        messages.error(request, 'คุณไม่มีสิทธิ์ทำรายการนี้')
        return redirect('tenants:tenant_home')

    if request.method == 'POST':
        # อัปเดต Payment
        payment.status = 'paid'
        payment.paid_date = timezone.now().date()
        payment.save()

        # อัปเดต Billing ฝั่ง app invoices
        try:
            from apps.invoices.models import Billing

            billing = Billing.objects.filter(
                room=payment.room,
                is_paid=False
            ).order_by('-service_month', '-id').first()

            if billing:
                billing.is_paid = True
                if hasattr(billing, 'paid_date'):
                    billing.paid_date = timezone.now()
                billing.save()
        except Exception:
            pass

        # อัปเดต Invoice ใน app payments (ถ้ามีใช้งานอยู่)
        try:
            invoice = Invoice.objects.filter(
                tenant=tenant,
                room=payment.room,
                status__in=['unpaid', 'overdue']
            ).order_by('-invoice_date').first()

            if invoice:
                invoice.status = 'paid'
                invoice.save()
        except Exception:
            pass

        messages.success(request, 'ชำระเงินเรียบร้อยแล้ว')
        return redirect('tenants:tenant_home')

    return redirect('tenants:tenant_home')


# ==========================================
# 2. Meter Views
# ==========================================
@login_required
def meter_list(request):
    meters = Meter.objects.select_related('tenant', 'room').all()
    return render(request, 'meters/meter_list.html', {'meters': meters})


@login_required
def meter_detail(request, pk):
    meter = get_object_or_404(Meter, pk=pk)
    return render(request, 'meters/meter_detail.html', {'meter': meter})


@login_required
def meter_create(request):
    if request.method == 'POST':
        form = MeterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกเลขมิเตอร์เรียบร้อย')
            return redirect('payments:meter_list')
    else:
        form = MeterForm()

    return render(request, 'meters/meter_form.html', {
        'form': form,
        'title': 'Add Meter Reading'
    })


@login_required
def meter_edit(request, pk):
    meter = get_object_or_404(Meter, pk=pk)

    if request.method == 'POST':
        form = MeterForm(request.POST, instance=meter)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขเลขมิเตอร์เรียบร้อย')
            return redirect('payments:meter_list')
    else:
        form = MeterForm(instance=meter)

    return render(request, 'meters/meter_form.html', {
        'form': form,
        'title': 'Edit Meter Reading'
    })


@login_required
def meter_delete(request, pk):
    meter = get_object_or_404(Meter, pk=pk)

    if request.method == 'POST':
        meter.delete()
        messages.success(request, 'ลบเลขมิเตอร์เรียบร้อย')
        return redirect('payments:meter_list')

    return render(request, 'meters/meter_confirm_delete.html', {
        'meter': meter
    })


# ==========================================
# 3. Invoice Views
# ==========================================
@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('tenant', 'room').all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ออกใบแจ้งหนี้เรียบร้อย')
            return redirect('payments:invoice_list')
    else:
        form = InvoiceForm()

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'title': 'Add Invoice'
    })


@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขใบแจ้งหนี้เรียบร้อย')
            return redirect('payments:invoice_list')
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'title': 'Edit Invoice'
    })


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'ลบใบแจ้งหนี้เรียบร้อย')
        return redirect('payments:invoice_list')

    return render(request, 'invoices/invoice_confirm_delete.html', {
        'invoice': invoice
    })


# ==========================================
# 4. Maintenance Views
# ==========================================
@login_required
def maintenance_list(request):
    pending = Maintenance.objects.filter(status='pending').select_related('tenant', 'room')
    completed = Maintenance.objects.filter(status='completed').select_related('tenant', 'room')

    return render(request, 'payments/maintenance_list.html', {
        'pending': pending,
        'completed': completed
    })


@login_required
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'payments/maintenance_detail.html', {'maintenance': maintenance})


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ส่งเรื่องแจ้งซ่อมเรียบร้อย')
            return redirect('payments:maintenance_list')
    else:
        form = MaintenanceForm()

    return render(request, 'payments/maintenance_form.html', {
        'form': form,
        'title': 'Add Maintenance Request'
    })


@login_required
def maintenance_edit(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)

    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสถานะแจ้งซ่อมเรียบร้อย')
            return redirect('payments:maintenance_list')
    else:
        form = MaintenanceForm(instance=maintenance)

    return render(request, 'payments/maintenance_form.html', {
        'form': form,
        'title': 'Edit Maintenance Request'
    })


@login_required
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)

    if request.method == 'POST':
        maintenance.delete()
        messages.success(request, 'ลบรายการแจ้งซ่อมเรียบร้อย')
        return redirect('payments:maintenance_list')

    return render(request, 'payments/maintenance_confirm_delete.html', {
        'maintenance': maintenance
    })