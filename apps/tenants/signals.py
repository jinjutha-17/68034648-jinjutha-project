from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tenant , UserProfile
from apps.rooms.models import Room
from django.contrib.auth.models import User

@receiver(post_save, sender=Tenant)
def sync_room_status_on_save(sender, instance, created, **kwargs):
    """Update room status to 'Occupied' when a tenant is assigned."""
    if instance.room:
        instance.room.status = 'ไม่ว่าง'
        instance.room.save()

@receiver(post_delete, sender=Tenant)
def sync_room_status_on_delete(sender, instance, **kwargs):
    """Update room status to 'Vacant' when a tenant is deleted/removed."""
    if instance.room:
        # Check if there are other active tenants in this room (unlikely with OneToOne, but for safety)
        instance.room.status = 'ว่าง'
        instance.room.save()

@receiver(post_save, sender=Tenant)
def create_user_for_tenant(sender, instance, created, **kwargs):
    if created and not instance.user:
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password='1234'
        )

        # assign user ให้ tenant
        instance.user = user
        instance.save()

        # สร้าง profile
        UserProfile.objects.create(
            user=user,
            role='Tenant'
        )
