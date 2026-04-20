from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('add/', views.booking_create, name='create'),
    path('<int:pk>/edit/', views.booking_edit, name='edit'),
    path('<int:pk>/delete/', views.booking_delete, name='delete'),
]
