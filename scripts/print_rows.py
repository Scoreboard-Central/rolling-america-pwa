import re

with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]
for i in [2,3,4,8,9]:
    arr = lines[i].split()
    print(f"R{i:02d}: " + " ".join(f"{c}({j})" for j, c in enumerate(arr)))

