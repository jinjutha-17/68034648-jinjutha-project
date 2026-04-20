from django.urls import path
from . import views

app_name = 'meters'

urlpatterns = [
    path('', views.meter_list, name='meter_list'),
    path('add/', views.meter_create, name='meter_create'),
    path('<int:pk>/edit/', views.meter_edit, name='meter_edit'),
    path('<int:pk>/delete/', views.meter_delete, name='meter_delete'),
]