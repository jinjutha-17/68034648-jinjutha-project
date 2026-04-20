from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('', views.tenant_list, name='list'),
    path('home/', views.tenant_home, name='tenant_home'),
    path('my/', views.my_profile, name='my_profile'),
    path('choose-room/', views.choose_room, name='choose_room'),
    path('select-room/<int:pk>/', views.select_room, name='select_room'),
    path('create/', views.tenant_create, name='create'),
    path('<int:pk>/', views.tenant_detail, name='detail'),
    path('<int:pk>/edit/', views.tenant_edit, name='edit'),
    path('<int:pk>/delete/', views.tenant_delete, name='delete'),
]