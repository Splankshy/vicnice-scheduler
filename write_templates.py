f = open('scheduler/templates/scheduler/appointments.html', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    '<a href="/appointments/{{ a.pk }}/edit/"',
    '<a href="/appointments/{{ a.pk }}/remind/" style="background:#059669;color:white;border:none;padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;text-decoration:none;margin-right:4px;">Remind</a><a href="/appointments/{{ a.pk }}/edit/"'
)
f = open('scheduler/templates/scheduler/appointments.html', 'w', encoding='utf-8')
f.write(content)
f.close()
print('remind button added!')