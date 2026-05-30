import os

for filename in ['appointments', 'clients', 'students', 'calendar']:
    path = f'scheduler/templates/scheduler/{filename}.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('<table>', '<div class="table-wrap"><table>')
    content = content.replace('</table>', '</table></div>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{filename}.html updated!')