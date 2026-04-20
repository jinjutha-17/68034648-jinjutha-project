from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


@login_required
def booking_list(request):
    bookings = Booking.objects.select_related('room').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'status_filter': status_filter})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created successfully.')
            return redirect('bookings:list')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'title': 'New Booking'})


@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated.')
            return redirect('bookings:list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form, 'title': 'Edit Booking'})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted.')
        return redirect('bookings:list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
