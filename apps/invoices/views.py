from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
import datetime

from .models import Billing
from apps.rooms.models import Room
from apps.meters.models import Meter


# 📊 LIST
def billing_list(request):
    billings = Billing.objects.select_related('room', 'meter').order_by('-service_month', '-id')
    return render(request, 'invoices/billing_list.html', {'data': billings})


# ⚡ CREATE BILL (ใช้ Meter ใหม่)
def create_billing(request):
    today = datetime.date.today()
    rooms = Room.objects.all()

    for room in rooms:
        meter = Meter.objects.filter(room=room).order_by('-reading_date').first()

        if not meter:
            continue

        exists = Billing.objects.filter(
            room=room,
            service_month__month=today.month,
            service_month__year=today.year
        ).exists()

        if exists:
            continue

        Billing.objects.create(
            room=room,
            meter=meter,
            total_amount=meter.total_amount
        )

    return redirect('invoices:billing_list')


# 💸 PAY
def pay_bill(request, billing_id):
    if request.method == 'POST':
        bill = get_object_or_404(Billing, pk=billing_id)

        if not bill.is_paid:
            bill.is_paid = True
            bill.paid_date = timezone.now()
            bill.save()

    return redirect('invoices:billing_list')


# 📄 PDF
def export_billing_pdf(request, billing_id):
    bill = get_object_or_404(Billing, pk=billing_id)

    meter = bill.meter

    elec_units = meter.reading_value if meter else 0
    water_units = meter.water_charge if meter else 0

    context = {
        'bill': bill,
        'elec_units': elec_units,
        'water_units': water_units,
        'today': datetime.date.today(),
    }

    template = get_template('invoices/pdf_template.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Invoice_{bill.room.room_number}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response