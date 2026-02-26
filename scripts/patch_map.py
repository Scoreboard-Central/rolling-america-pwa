import re

with open('make_map.py', 'r') as f:
    make_code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', make_code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid_str = "\n".join(lines).strip()

with open('generate_map.py', 'r') as f:
    gen_code = f.read()

# Replace between grid_str = """ and """
new_gen_code = re.sub(r'grid_str = """[\s\S]*?"""', f'grid_str = """\n{grid_str}\n"""', gen_code)

with open('generate_map.py', 'w') as f:
    f.write(new_gen_code)

print("Patched generate_map.py successfully.")
