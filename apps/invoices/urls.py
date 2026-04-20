from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('create/', views.create_billing, name='create_billing'),
    path('pay/<int:billing_id>/', views.pay_bill, name='pay_bill'),
    path('pdf/<int:billing_id>/', views.export_billing_pdf, name='export_billing_pdf'),
]