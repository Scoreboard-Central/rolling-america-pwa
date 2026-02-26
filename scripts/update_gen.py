import re

with open('make_map.py', 'r') as f: code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
# clean up to just the space-separated words
lines = [" ".join(l.split()) for l in lines]
grid_str = "\n".join(lines)

with open('generate_map.py', 'r') as f:
    gen_code = f.read()

new_gen_code = re.sub(r'grid_str = """[\s\S]*?"""', f'grid_str = """\n{grid_str}\n"""', gen_code)
# Set SIZE back to 34 or something suitable for a 16x32 grid
# The original generate_map.py uses SIZE = 34
with open('generate_map.py', 'w') as f:
    f.write(new_gen_code)

print("Updated generate_map.py!")
