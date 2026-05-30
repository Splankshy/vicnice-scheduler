import calendar as cal
from datetime import date

f = open('scheduler/views.py', 'r', encoding='utf-8')
content = f.read()
f.close()

old = '''@login_required
def calendar_view(request):
    appointments = Appointment.objects.all().order_by("date")
    return render(request, "scheduler/calendar.html", {"appointments": appointments})'''

new = '''@login_required
def calendar_view(request):
    import calendar as cal_module
    from datetime import date
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
    return render(request, "scheduler/calendar.html", context)'''

content = content.replace(old, new)
f = open('scheduler/views.py', 'w', encoding='utf-8')
f.write(content)
f.close()
print('calendar view updated!')