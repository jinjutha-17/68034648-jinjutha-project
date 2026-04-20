from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Meter
from .forms import MeterForm
from apps.payments.models import Payment


def create_payment_from_meter(meter):
    room = meter.room
    tenant = meter.tenant

    if not room or not tenant:
        return

    rent = Decimal(str(getattr(room, 'monthly_rent', 0) or 0))
    electric = Decimal(str(meter.reading_value or 0)) * Decimal('7.00')
    water = Decimal(str(meter.water_charge or 0)) * Decimal('18.00')

    total = rent + electric + water
    today = timezone.now().date()

    payment = Payment.objects.filter(
        tenant=tenant,
        room=room,
        due_date__year=today.year,
        due_date__month=today.month
    ).first()

    if payment:
        payment.amount = total
        payment.status = 'pending'
        payment.payment_type = 'rent'
        payment.due_date = today
        payment.save()
    else:
        Payment.objects.create(
            tenant=tenant,
            room=room,
            amount=total,
            status='pending',
            due_date=today,
            payment_type='rent'
        )


@login_required
def meter_list(request):
    meters = Meter.objects.select_related('room', 'tenant').order_by('-reading_date')

    search = request.GET.get('search', '')
    if search:
        meters = meters.filter(room__room_number__icontains=search)

    paginator = Paginator(meters, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'meters/meter_list.html', {
        'page_obj': page_obj,
        'search': search
    })


@login_required
def meter_create(request):
    if request.method == 'POST':
        form = MeterForm(request.POST)
        if form.is_valid():
            meter = form.save()
            create_payment_from_meter(meter)
            messages.success(request, 'Meter reading recorded successfully and tenant payment updated.')
            return redirect('meters:meter_list')
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
            meter = form.save()
            create_payment_from_meter(meter)
            messages.success(request, 'Meter reading updated and tenant payment recalculated.')
            return redirect('meters:meter_list')
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
        messages.success(request, 'Meter reading deleted.')
        return redirect('meters:meter_list')

    return render(request, 'meters/meter_confirm_delete.html', {
        'meter': meter
    })