from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    measurements = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    enrolled = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    TYPE_CHOICES = [
        ('consultation', 'Client Consultation'),
        ('fitting', 'Fitting Session'),
        ('sewing', 'Sewing & Production'),
        ('class', 'Training Class'),
        ('delivery', 'Delivery / Pickup'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title