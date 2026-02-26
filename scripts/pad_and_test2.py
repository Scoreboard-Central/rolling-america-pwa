import re
with open('make_map.py', 'r') as f:
    code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]

lines_split = [l.split() for l in lines]
for y in range(len(lines_split)):
    for x in range(len(lines_split[y])):
        if lines_split[y][x] == 'IN':
            print(f"IN at {y},{x}")
        if lines_split[y][x] == 'KY':
            print(f"KY at {y},{x}")
