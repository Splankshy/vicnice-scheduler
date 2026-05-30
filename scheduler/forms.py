from django import forms
from .models import Appointment, Client, Student, StaffMember

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'type', 'status', 'date', 'start_time', 'end_time', 'client', 'student', 'staff', 'location', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'measurements', 'notes']
        widgets = {
            'measurements': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'email', 'level', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }