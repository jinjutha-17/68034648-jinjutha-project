from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('add/', views.payment_create, name='create'),
    path('<int:pk>/edit/', views.payment_edit, name='edit'),
    path('<int:pk>/delete/', views.payment_delete, name='delete'),
    path('<int:pk>/approve/', views.payment_approve, name='approve'),

    path('tenant/', views.tenant_payment_list, name='tenant_payment_list'),
    path('tenant/create/', views.tenant_payment_create, name='tenant_payment_create'),
    path('tenant/<int:pk>/submit/', views.tenant_payment_submit, name='tenant_payment_submit'),

    path('meters/', views.meter_list, name='meter_list'),
    path('meters/<int:pk>/', views.meter_detail, name='meter_detail'),
    path('meters/add/', views.meter_create, name='meter_create'),
    path('meters/<int:pk>/edit/', views.meter_edit, name='meter_edit'),
    path('meters/<int:pk>/delete/', views.meter_delete, name='meter_delete'),

    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/add/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),

    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/add/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
    path('maintenance/<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),
]