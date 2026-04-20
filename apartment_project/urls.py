from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import login_view, register_view
from apps.tenants.views import tenant_home

urlpatterns = [
    path('admin/', admin.site.urls),

    # หน้าแรก → ไป login
    path('', RedirectView.as_view(url=settings.LOGIN_URL, permanent=False)),

    # Root-level auth
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    # Tenant portal
    path('tenant-portal/', tenant_home, name='tenant_home'),

    # App inclusions
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('rooms/', include('apps.rooms.urls')),
    path('tenants/', include('apps.tenants.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('payments/', include('apps.payments.urls')),
    path('meters/', include('apps.meters.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('parcels/', include('apps.parcels.urls')),

    #  จุดที่แก้
    path('repairs/', include('apps.repairs.urls')),
    path('maintenance/', include('apps.repairs.urls')),  # alias ใหม่

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)