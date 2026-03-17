import pathlib

content = pathlib.Path('app.py').read_text(encoding='utf-8')
lines = content.split('\n')

for i, line in enumerate(lines):
    if 'font-size:38px; margin-bottom:6px;' in line and '📊' not in line:
        lines[i] = line.replace('margin-bottom:6px;></div>', 'margin-bottom:6px;">📊</div>')

content = '\n'.join(lines)
pathlib.Path('app.py').write_text(content, encoding='utf-8')
print('✅ Emoji corrigido')
