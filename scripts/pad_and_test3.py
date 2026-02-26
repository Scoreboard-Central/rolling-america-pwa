import re
with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]
fixed = [l.split() for l in lines]
fixed[6][20] = 'IN'
fixed[6][19] = 'IL' # move IL right to touch IN
joined = ",\n    ".join('"' + " ".join(r) + '"' for r in fixed)
new_code = re.sub(r'grid_lines = \[(.*?)\]', f'grid_lines = [\n    {joined}\n]', code, flags=re.DOTALL)
with open('make_map.py', 'w') as f: f.write(new_code)
