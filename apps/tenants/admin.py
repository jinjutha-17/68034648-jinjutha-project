from django.contrib import admin
from .models import Tenant, Contract, UserProfile, EmployeePermission


class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'room', 'is_active')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'tenant', 'room', 'start_date', 'end_date', 'status')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


class EmployeePermissionAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmployeePermission, EmployeePermissionAdmin)