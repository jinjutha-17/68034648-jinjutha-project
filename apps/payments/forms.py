from django import forms
from .models import Payment, Meter, Invoice, Maintenance


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['tenant', 'room', 'payment_type', 'amount', 'due_date', 'paid_date', 'status', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['tenant', 'room', 'previous_reading', 'current_reading', 'reading_date', 'notes']
        widgets = {
            'reading_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['tenant', 'room', 'invoice_date', 'due_date', 'amount', 'status', 'notes']
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['tenant', 'room', 'issue', 'description', 'status', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
