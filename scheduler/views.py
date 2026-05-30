from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Client, Student, StaffMember, Appointment
from .forms import AppointmentForm, ClientForm, StudentForm
from datetime import date

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "scheduler/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    today = timezone.now().date()
    todays = Appointment.objects.filter(date=today)
    upcoming = Appointment.objects.filter(date__gte=today).order_by("date")[:5]
    total_clients = Client.objects.count()
    total_students = Student.objects.count()
    total_appointments = Appointment.objects.count()
    context = {
        "todays": todays,
        "upcoming": upcoming,
        "total_clients": total_clients,
        "total_students": total_students,
        "total_appointments": total_appointments,
        "today": today,
    }
    return render(request, "scheduler/dashboard.html", context)

@login_required
def appointments(request):
    query = request.GET.get("q", "")
    all_appointments = Appointment.objects.all().order_by("-date")
    if query:
        all_appointments = all_appointments.filter(
            Q(title__icontains=query) | Q(location__icontains=query) |
            Q(client__name__icontains=query) | Q(student__name__icontains=query)
        )
    form = AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("appointments")
    return render(request, "scheduler/appointments.html", {"appointments": all_appointments, "form": form, "query": query})

@login_required
def delete_appointment(request, pk):
    a = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        a.delete()
    return redirect("appointments")

@login_required
def edit_appointment(request, pk):
    a = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(instance=a)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect("appointments")
    return render(request, "scheduler/edit_appointment.html", {"form": form, "appointment": a})

@login_required
def print_appointments(request):
    appointments = Appointment.objects.all().order_by("date")
    return render(request, "scheduler/print_appointments.html", {
        "appointments": appointments,
        "today": date.today().strftime("%B %d, %Y")
    })

@login_required
def send_reminder(request, pk):
    a = get_object_or_404(Appointment, pk=pk)
    recipient = None
    name = None
    if a.client and a.client.email:
        recipient = a.client.email
        name = a.client.name
    elif a.student and a.student.email:
        recipient = a.student.email
        name = a.student.name
    if recipient:
        subject = f"Reminder: {a.title} on {a.date}"
        message = f"Dear {name},\n\nThis is a reminder for your upcoming appointment at Vic_nice Home Concepts.\n\nAppointment: {a.title}\nType: {a.get_type_display()}\nDate: {a.date}\nTime: {a.start_time or chr(39)}TBD{chr(39)}\nLocation: {a.location or chr(39)}Vic_nice Studio{chr(39)}\n\nPlease contact us if you need to reschedule.\n\nBest regards,\nVic_nice Home Concepts"
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
            messages.success(request, f"Reminder sent to {recipient}!")
        except Exception as e:
            messages.error(request, f"Failed to send: {str(e)}")
    else:
        messages.error(request, "No email address found for this appointment.")
    return redirect("appointments")

@login_required
def clients(request):
    query = request.GET.get("q", "")
    all_clients = Client.objects.all().order_by("name")
    if query:
        all_clients = all_clients.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query)
        )
    form = ClientForm()
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clients")
    return render(request, "scheduler/clients.html", {"clients": all_clients, "form": form, "query": query})

@login_required
def delete_client(request, pk):
    c = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        c.delete()
    return redirect("clients")

@login_required
def students(request):
    query = request.GET.get("q", "")
    all_students = Student.objects.all().order_by("name")
    if query:
        all_students = all_students.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query)
        )
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("students")
    return render(request, "scheduler/students.html", {"students": all_students, "form": form, "query": query})

@login_required
def delete_student(request, pk):
    s = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        s.delete()
    return redirect("students")

@login_required
def calendar_view(request):
    import calendar as cal_module
    today = date.today()
    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))
    if month < 1:
        month = 12
        year -= 1
    if month > 12:
        month = 1
        year += 1
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year
    first_weekday, days_in_month = cal_module.monthrange(year, month)
    first_weekday = (first_weekday + 1) % 7
    calendar_days = [0] * first_weekday + list(range(1, days_in_month + 1))
    appointments = Appointment.objects.all().order_by("date")
    month_appointments = appointments.filter(date__month=month, date__year=year)
    days_with_events = set(a.date.day for a in month_appointments)
    context = {
        "appointments": appointments,
        "month_appointments": month_appointments,
        "calendar_days": calendar_days,
        "month": month,
        "year": year,
        "month_name": cal_module.month_name[month],
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
        "today_day": today.day,
        "today_month": today.month,
        "today_year": today.year,
        "days_with_events": days_with_events,
    }
    return render(request, "scheduler/calendar.html", context)

def setup(request):
    if User.objects.filter(is_superuser=True).exists():
        return redirect("dashboard")
    if request.method == "POST":
        key = request.POST.get("key")
        if key != "vicnice2026":
            messages.error(request, "Wrong setup key!")
            return render(request, "scheduler/setup.html")
        username = request.POST.get("username")
        email = request.POST.get("email", "")
        password = request.POST.get("password")
        User.objects.create_superuser(username=username, email=email, password=password)
        messages.success(request, "Admin account created! You can now log in.")
        return redirect("/admin/")
    return render(request, "scheduler/setup.html")
