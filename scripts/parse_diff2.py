import sys
rules = {}
with open('state_color_rules.txt', 'r') as f:
    lines = f.readlines()
    current_state = None
    for line in lines:
        if line.startswith('State: '):
            current_state = line.split()[1]
            rules[current_state] = []
        elif line.strip().startswith('Neighbor States:'):
            n_str = line.split(':', 1)[1].strip()
            if n_str:
                rules[current_state] = [n.strip() for n in n_str.split(',')]

import ast
with open('build_strict_grid.py', 'r') as f: code = f.read()
import re
m = re.search(r'image_neighbors = (\{.*?\})', code, flags=re.DOTALL)
img_n = ast.literal_eval(m.group(1))

# what are the diffs between the user's rules and the original perfect graph?
diffs = 0
for s, neighbors in rules.items():
    if s in ['AK', 'HI']: continue
    expected = img_n.get(s, set())
    actual = set(neighbors)
    if expected != actual:
        diffs += 1
        print(f"{s}: Expected {expected}, User provided {actual}")
