from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RoomForm
from .models import Room
from django.db.models import Q

@login_required
def room_list(request):
    rooms = Room.objects.select_related('current_tenant').order_by('floor', 'room_number')
    status_filter = request.GET.get('status', '')
    floor_filter = request.GET.get('floor', '')
    search_query = request.GET.get('search', '').strip()

    if status_filter:
        rooms = rooms.filter(status=status_filter)
    if floor_filter:
        rooms = rooms.filter(floor=floor_filter)
    if search_query:
        rooms = rooms.filter(
        Q(room_number__icontains=search_query) |
        Q(current_tenant__first_name__icontains=search_query) |
        Q(current_tenant__last_name__icontains=search_query)
    )
        
    rooms_by_floor = {}
    for room in rooms:
        if room.floor not in rooms_by_floor:
            rooms_by_floor[room.floor] = []
        rooms_by_floor[room.floor].append(room)

    context = {
        'rooms_by_floor': rooms_by_floor,
        'status_filter': status_filter,
        'search_query': search_query,
        'floor_filter': floor_filter,
        'floors': Room.objects.values_list('floor', flat=True).distinct().order_by('floor'),
        'available_count': Room.objects.filter(status='ว่าง').count(),
        'occupied_count': Room.objects.filter(status='ไม่ว่าง').count(),
        'maintenance_count': Room.objects.filter(status='ซ่อมบำรุง').count(),
        'total_rooms': Room.objects.count(),
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', {'room': room})


@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully.')
            return redirect('rooms:list')
    else:
        form = RoomForm()
    return render(request, 'rooms/room_form.html', {'form': form, 'title': 'Add Room'})


@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated.')
            return redirect('rooms:list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/room_form.html', {'form': form, 'title': 'Edit Room'})


@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted.')
        return redirect('rooms:list')
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})
