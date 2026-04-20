from django.contrib import admin
from django.utils.html import format_html

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number',
        'image_preview',
        'floor',
        'room_type',
        'monthly_rent',
        'status_badge',
        'created_at',
    )
    list_filter = ('floor', 'status', 'room_type')
    search_fields = ('room_number', 'description')
    readonly_fields = ('image_preview_large', 'created_at')

    fieldsets = (
        ('ข้อมูลห้องพัก', {
            'fields': ('room_number', 'floor', 'room_type', 'size_sqm', 'monthly_rent', 'status')
        }),
        ('รายละเอียดเพิ่มเติม', {
            'fields': ('description', 'image', 'image_preview_large', 'created_at')
        }),
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:10px;" />', obj.image.url)
        return format_html('<span style="color:#94a3b8;">ไม่มีรูป</span>')
    image_preview.short_description = 'รูปภาพ'

    def image_preview_large(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-width:240px;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.12);" />', obj.image.url)
        return 'ยังไม่ได้อัปโหลดรูปภาพ'
    image_preview_large.short_description = 'ตัวอย่างรูปภาพ'

    def status_badge(self, obj):
        color_map = {
            'available': ('#dcfce7', '#166534', 'ว่าง'),
            'occupied': ('#dbeafe', '#1d4ed8', 'มีผู้เช่า'),
            'maintenance': ('#fee2e2', '#b91c1c', 'ซ่อมบำรุง'),
        }
        background, text, label = color_map.get(obj.status, ('#e2e8f0', '#334155', obj.status))
        return format_html(
            '<span style="background:{};color:{};padding:4px 10px;border-radius:999px;font-weight:600;">{}</span>',
            background,
            text,
            label,
        )
    status_badge.short_description = 'สถานะ'
