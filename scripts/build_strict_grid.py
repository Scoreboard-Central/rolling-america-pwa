import sys

# Color lookup to verify counts
colors = {
    'AK': 'orange', 'HI': 'orange', 'WA': 'orange', 'OR': 'orange', 'ID': 'orange', 'UT': 'orange', 'AZ': 'orange', 'NV': 'orange', 'CA': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'IN': 'blue', 'MI': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green',
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'AL': 'yellow', 'TN': 'yellow', 'MS': 'yellow', 'FL': 'yellow', 'KY': 'yellow',
    'DE': 'red', 'MD': 'red', 'PA': 'red', 'OH': 'red', 'WV': 'red', 'VA': 'red', 'NC': 'red', 'SC': 'red', 'GA': 'red',
    'ME': 'purple', 'NH': 'purple', 'VT': 'purple', 'NY': 'purple', 'MA': 'purple', 'RI': 'purple', 'CT': 'purple', 'NJ': 'purple',
}

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME .. .. .. .. .. ..
.. .. AK AK AK AK .. .. WA WA WA WA ID ID ID ID MT MT MT MT ND ND ND ND MN MN MN MN WI WI WI WI MI MI MI MI NY NY VT VT NH NH ME ME .. ..
.. .. AK AK AK AK .. .. WA WA WA WA ID ID ID ID MT MT MT MT ND ND ND ND MN MN MN MN WI WI WI WI MI MI MI MI NY NY VT VT NH NH ME ME .. ..
.. .. AK AK AK AK .. .. OR OR OR OR ID ID ID ID WY WY WY WY SD SD SD SD IA IA IA IA IL IL IL IL IN IN MI MI NY NY MA MA MA MA ME ME .. ..
.. .. AK AK AK AK .. .. OR OR OR OR ID ID ID ID WY WY WY WY SD SD SD SD IA IA IA IA IL IL IL IL IN IN MI MI NY NY MA MA MA MA ME ME .. ..
.. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV UT UT UT UT CO CO CO CO NE NE NE NE IA IA IA IA IN IN OH OH PA PA CT CT CT CT RI RI .. ..
.. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV UT UT UT UT CO CO CO CO NE NE NE NE IA IA IA IA IN IN OH OH PA PA CT CT CT CT RI RI .. ..
.. .. HI HI HI HI .. .. CA CA CA CA NV NV NV NV AZ AZ AZ AZ NM NM OK OK KS KS KS KS MO MO MO MO KY KY OH OH PA PA NJ NJ CT CT RI RI .. ..
.. .. HI HI HI HI .. .. CA CA CA CA NV NV NV NV AZ AZ AZ AZ NM NM OK OK KS KS KS KS MO MO MO MO KY KY OH OH PA PA NJ NJ CT CT RI RI .. ..
.. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ NM NM OK OK OK OK AR AR AR AR MO MO MO MO KY KY WV WV MD MD MD MD DE DE DE DE .. ..
.. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ NM NM OK OK OK OK AR AR AR AR MO MO MO MO KY KY WV WV MD MD MD MD DE DE DE DE .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ TX TX TX TX TX TX AR AR AR AR LA LA TN TN TN TN TN TN VA VA VA VA VA VA .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ TX TX TX TX TX TX AR AR AR AR LA LA TN TN TN TN TN TN VA VA VA VA VA VA .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX AR AR AR AR LA LA MS MS MS MS AL AL NC NC NC NC NC NC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX AR AR AR AR LA LA MS MS MS MS AL AL NC NC NC NC NC NC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA MS MS MS MS AL AL GA GA SC SC SC SC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA MS MS MS MS AL AL GA GA SC SC SC SC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AL AL GA GA GA GA SC SC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AL AL GA GA SC SC SC SC .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. GA GA FL FL FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. GA GA FL FL FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. .. .. .. ..
"""

lines = [l.strip().split() for l in grid_str.strip().split('\n')]
# uniform width
W = max(len(l) for l in lines)
H = len(lines)
grid = [r + ['..']*(W-len(r)) for r in lines]

for r in grid:
    print(" ".join(f"{c:2}" for c in r))

states = set(c for r in grid for c in r if c != '..')
for s in colors.keys():
    if s not in states:
        print(f"MISSING STATE: {s}")

# Neighbors from picture (very meticulous definition)
# Every state and what it MUST border in the picture
image_neighbors = {
    'WA': {'OR', 'ID', 'MT'},
    'OR': {'WA', 'ID', 'CA', 'NV'},
    'CA': {'OR', 'NV', 'AZ'},
    'NV': {'OR', 'ID', 'UT', 'CA', 'AZ'},
    'ID': {'WA', 'MT', 'OR', 'WY', 'NV', 'UT'}, # Wait, does ID touch UT? Yes, picture shows ID is above NV, UT, WY
    'UT': {'ID', 'WY', 'CO', 'NV', 'AZ', 'NM'},
    'AZ': {'NV', 'UT', 'CA', 'NM'},
    'MT': {'WA', 'ID', 'WY', 'ND', 'SD'},
    'WY': {'MT', 'ID', 'SD', 'NE', 'UT', 'CO'},
    'CO': {'WY', 'NE', 'KS', 'OK', 'UT', 'NM'},
    'NM': {'CO', 'OK', 'TX', 'UT', 'AZ'},
    'ND': {'MT', 'SD', 'MN'},
    'SD': {'ND', 'MT', 'WY', 'MN', 'IA', 'NE'},
    'NE': {'SD', 'WY', 'CO', 'IA', 'MO', 'KS'},
    'KS': {'NE', 'CO', 'OK', 'MO'},
    'OK': {'KS', 'CO', 'NM', 'MO', 'AR', 'TX'},
    'TX': {'OK', 'NM', 'AR', 'LA'},
    'MN': {'ND', 'SD', 'IA', 'WI'},
    'IA': {'MN', 'SD', 'NE', 'WI', 'IL', 'MO'},
    'MO': {'IA', 'NE', 'KS', 'OK', 'AR', 'IL', 'KY', 'TN'},
    'AR': {'MO', 'OK', 'TX', 'TN', 'MS', 'LA'},
    'LA': {'AR', 'TX', 'MS'},
    'WI': {'MN', 'IA', 'IL', 'MI'},
    'IL': {'WI', 'IA', 'MO', 'MI', 'IN', 'KY'}, # Does IL touch MI? Image says no, wait, image says IL touches WI, IN. MI is above IN. Let's assume IL touches MI via lake. Let's stick to standard grid for now or ignore strictly exact edges if they are trivial, but the user said "MAKE SURE THOSE RULES ARE FOLLOWED".
    'MI': {'WI', 'IL', 'IN', 'OH'},
    'IN': {'MI', 'IL', 'OH', 'KY'},
    'OH': {'MI', 'IN', 'PA', 'WV', 'KY'},
    'KY': {'IN', 'OH', 'WV', 'VA', 'IL', 'MO', 'TN'},
    'TN': {'KY', 'VA', 'NC', 'MO', 'AR', 'MS', 'AL', 'GA'},
    'MS': {'TN', 'AR', 'LA', 'AL'},
    'AL': {'TN', 'MS', 'GA', 'FL'},
    'FL': {'AL', 'GA'},
    'PA': {'NY', 'NJ', 'OH', 'WV', 'MD', 'DE'},
    'WV': {'OH', 'PA', 'MD', 'VA', 'KY'},
    'VA': {'MD', 'WV', 'KY', 'TN', 'NC'},
    'NC': {'VA', 'TN', 'GA', 'SC'},
    'SC': {'NC', 'GA'},
    'GA': {'NC', 'SC', 'TN', 'AL', 'FL'},
    'NY': {'VT', 'MA', 'CT', 'NJ', 'PA'},
    'NJ': {'NY', 'PA', 'DE'},
    'DE': {'NJ', 'PA', 'MD'},
    'MD': {'PA', 'DE', 'WV', 'VA'},
    'CT': {'MA', 'RI', 'NY'},
    'RI': {'MA', 'CT'},
    'MA': {'NH', 'VT', 'NY', 'CT', 'RI'},
    'VT': {'NH', 'MA', 'NY'},
    'NH': {'ME', 'VT', 'MA'},
    'ME': {'NH'},
    'AK': set(),
    'HI': set(),
}

# Add symmetric links
for s, neighs in list(image_neighbors.items()):
    for n in neighs:
        image_neighbors[n].add(s)

neighbors = {s: set() for s in states}
for y in range(H):
    for x in range(W):
        c = grid[y][x]
        if c == '..': continue
        
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            # We don't use diagonals for neighbors unless requested, but grid maps often have corner touches we want to catch or avoid.
            # Usually only orthogonal touches count in these shapes. Let's do orthogonal first.
            pass

        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W:
                nc = grid[ny][nx]
                if nc != '..' and nc != c:
                    neighbors[c].add(nc)

# Let's check color neighbors for EVERY STATE
for s in states:
    if s in ['AK', 'HI']: continue
    expected = image_neighbors.get(s, set())
    actual = neighbors[s]
    
    # Check if color counts of neighbors match
    def color_counts(n_set):
        cts = {}
        for n in n_set:
            c = colors[n]
            cts[c] = cts.get(c, 0) + 1
        return cts
        
    exp_c = color_counts(expected)
    act_c = color_counts(actual)
    
    if exp_c != act_c:
        print(f"ERROR {s}: Expected color neighbors {exp_c}, but got {act_c}. Expected {expected}, got {actual}")

with open('grid.txt', 'w') as f:
    for r in grid:
        f.write(" ".join(f"{c:2}" for c in r) + "\n")

