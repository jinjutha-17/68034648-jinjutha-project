from django.contrib import admin
from django.utils.html import format_html

from .models import Invoice, Maintenance, Meter, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'payment_type', 'amount', 'due_date', 'status_badge')
    list_filter = ('status', 'payment_type', 'room__floor')
    search_fields = ('tenant__first_name', 'tenant__last_name', 'room__room_number')
    ordering = ('-due_date',)

    def status_badge(self, obj):
        palette = {
            'paid': ('#dcfce7', '#166534', 'ชำระแล้ว'),
            'pending': ('#fef3c7', '#92400e', 'รอชำระ'),
            'overdue': ('#fee2e2', '#b91c1c', 'ค้างชำระ'),
        }
        background, text, label = palette.get(obj.status, ('#e2e8f0', '#334155', obj.status))
        return format_html(
            '<span style="background:{};color:{};padding:4px 10px;border-radius:999px;font-weight:600;">{}</span>',
            background,
            text,
            label,
        )
    status_badge.short_description = 'สถานะการจ่ายเงิน'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'invoice_date', 'due_date', 'amount', 'status')
    list_filter = ('status', 'room__floor')
    search_fields = ('tenant__first_name', 'tenant__last_name', 'room__room_number')


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('room', 'tenant', 'issue', 'status', 'reported_date')
    list_filter = ('status', 'room__floor')
    search_fields = ('issue', 'tenant__first_name', 'tenant__last_name', 'room__room_number')


@admin.register(Meter)
class PaymentMeterAdmin(admin.ModelAdmin):
    list_display = ('room', 'tenant', 'previous_reading', 'current_reading', 'units_consumed', 'reading_date')
    list_filter = ('room__floor', 'reading_date')
    search_fields = ('room__room_number', 'tenant__first_name', 'tenant__last_name')
