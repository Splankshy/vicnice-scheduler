from django.contrib import admin
from .models import Client, Student, StaffMember, Appointment
admin.site.register(Client)
admin.site.register(Student)
admin.site.register(StaffMember)
admin.site.register(Appointment)