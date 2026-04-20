from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('client/', views.client_dashboard, name='client_dashboard'),
   
]
