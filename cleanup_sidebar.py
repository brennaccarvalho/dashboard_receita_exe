import re

content = open('app.py', 'r', encoding='utf-8').read()

# Find and remove the header block 
lines = content.split('\n')
new_lines = []
skip_until_semana = False

for i, line in enumerate(lines):
    # Skip the broken icon header block
    if 'with st.sidebar:' in line and i > 500:  # Make sure we're in sidebar section
        new_lines.append(line)
        new_lines.append('    st.write("**Dashboard**")')
        new_lines.append('    st.markdown("<hr style=\'margin: 0.5rem 0;\' />", unsafe_allow_html=True)')
        new_lines.append('    ')
        # Skip next lines until we reach the week selection section
        skip_until_semana = True
        continue
    elif skip_until_semana and "Semana de referência" in line:
        new_lines.append(line)
        skip_until_semana = False
    elif skip_until_semana:
        continue
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)
open('app.py', 'w', encoding='utf-8').write(content)
print("✅ Sidebar limpo - ícone removido")
