from django.contrib import admin

from .models import Meter


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['room', 'tenant', 'reading_value', 'water_charge', 'total_amount', 'reading_date']
    list_filter = ('room__floor', 'reading_date')
    search_fields = ('room__room_number', 'tenant__first_name', 'tenant__last_name')
    ordering = ('-reading_date',)