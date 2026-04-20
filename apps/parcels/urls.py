from django.urls import path
from . import views

urlpatterns = [
    path('', views.parcel_list, name='parcel_list'),
    path('add/', views.add_parcel, name='add_parcel'),
    path('confirm/<int:parcel_id>/', views.confirm_receipt, name='confirm_receipt'),
]
