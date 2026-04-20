from .models import Parcel


def parcel_context(request):
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role if hasattr(request.user, 'profile') else 'Admin'
            if role == 'Tenant':
                count = Parcel.objects.filter(
                    room__current_tenant__email=request.user.email,
                    status='pending'
                ).count()
            else:
                count = Parcel.objects.filter(status='pending').count()
        except Exception:
            count = 0
        return {'pending_parcels_count': count}
    return {'pending_parcels_count': 0}
