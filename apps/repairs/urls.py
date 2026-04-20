from django.urls import path
from . import views

app_name = 'repairs'

urlpatterns = [
    path('', views.repair_list, name='list'),
    path('create/', views.repair_create, name='create'),
    path('ajax-create/', views.ajax_create, name='ajax_create'),
    path('<int:pk>/edit/', views.repair_edit, name='edit'),
    path('<int:pk>/delete/', views.repair_delete, name='delete'),
]