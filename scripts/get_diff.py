import re

rules = {}
with open('state_color_rules.txt', 'r') as f:
    lines = f.readlines()
    
    current_state = None
    for line in lines:
        if line.startswith('State: '):
            current_state = line.split()[1]
            rules[current_state] = {'neighbors': [], 'edges': []}
        elif line.strip().startswith('Neighbor States:'):
            n_str = line.split(':', 1)[1].strip()
            rules[current_state]['neighbors'] = [n.strip() for n in n_str.split(',')]
        elif line.strip().startswith('Touches Edge:'):
            edge_str = line.split(':', 1)[1].strip()
            if edge_str != 'No':
                rules[current_state]['edges'] = edge_str.replace('Yes - ', '').split('/')

# compare with our old rules from build_strict_grid.py
old_neighbors = {
    'WA': {'OR', 'ID', 'MT'}, 'OR': {'WA', 'ID', 'CA', 'NV'}, 'CA': {'OR', 'NV', 'AZ'},
    'NV': {'OR', 'ID', 'UT', 'CA', 'AZ'}, 'ID': {'WA', 'MT', 'OR', 'WY', 'NV', 'UT'},
    'UT': {'ID', 'WY', 'CO', 'NV', 'AZ', 'NM'}, 'AZ': {'NV', 'UT', 'CA', 'NM'},
    'MT': {'WA', 'ID', 'WY', 'ND', 'SD'}, 'WY': {'MT', 'ID', 'SD', 'NE', 'UT', 'CO'},
    'CO': {'WY', 'NE', 'KS', 'OK', 'UT', 'NM'}, 'NM': {'CO', 'OK', 'TX', 'UT', 'AZ'},
    'ND': {'MT', 'SD', 'MN'}, 'SD': {'ND', 'MT', 'WY', 'MN', 'IA', 'NE'},
    'NE': {'SD', 'WY', 'CO', 'IA', 'MO', 'KS'}, 'KS': {'NE', 'CO', 'OK', 'MO'},
    'OK': {'KS', 'CO', 'NM', 'MO', 'AR', 'TX'}, 'TX': {'OK', 'NM', 'AR', 'LA'},
    'MN': {'ND', 'SD', 'IA', 'WI'}, 'IA': {'MN', 'SD', 'NE', 'WI', 'IL', 'MO'},
    'MO': {'IA', 'NE', 'KS', 'OK', 'AR', 'IL', 'KY', 'TN'}, 'AR': {'MO', 'OK', 'TX', 'TN', 'MS', 'LA'},
    'LA': {'AR', 'TX', 'MS'}, 'WI': {'MN', 'IA', 'IL', 'MI'},
    'IL': {'WI', 'IA', 'MO', 'MI', 'IN', 'KY'}, 'MI': {'WI', 'IL', 'IN', 'OH'},
    'IN': {'MI', 'IL', 'OH', 'KY'}, 'OH': {'MI', 'IN', 'PA', 'WV', 'KY'},
    'KY': {'IN', 'OH', 'WV', 'VA', 'IL', 'MO', 'TN'}, 'TN': {'KY', 'VA', 'NC', 'MO', 'AR', 'MS', 'AL', 'GA'},
    'MS': {'TN', 'AR', 'LA', 'AL'}, 'AL': {'TN', 'MS', 'GA', 'FL'}, 'FL': {'AL', 'GA'},
    'PA': {'NY', 'NJ', 'OH', 'WV', 'MD', 'DE', 'VA'}, 'WV': {'OH', 'PA', 'MD', 'VA', 'KY'},
    'VA': {'MD', 'WV', 'KY', 'TN', 'NC', 'PA'}, 'NC': {'VA', 'TN', 'GA', 'SC'}, 'SC': {'NC', 'GA'},
    'GA': {'NC', 'SC', 'TN', 'AL', 'FL'}, 'NY': {'VT', 'MA', 'CT', 'NJ', 'PA'},
    'NJ': {'NY', 'PA', 'DE', 'CT'}, 'DE': {'NJ', 'PA', 'MD'}, 'MD': {'PA', 'DE', 'WV', 'VA'},
    'CT': {'MA', 'RI', 'NY', 'NJ'}, 'RI': {'MA', 'CT'}, 'MA': {'NH', 'VT', 'NY', 'CT', 'RI'},
    'VT': {'NH', 'MA', 'NY'}, 'NH': {'ME', 'VT', 'MA'}, 'ME': {'NH'},
}
# ensure symmetry in old_neighbors
for s, ns in list(old_neighbors.items()):
    for n in ns:
        if n in old_neighbors:
            old_neighbors[n].add(s)

diffs = 0
for s, data in rules.items():
    if s in ['AK', 'HI']: continue
    new_n = set(data['neighbors'])
    old_n = old_neighbors.get(s, set())
    if new_n != old_n:
        print(f"Diff for {s}:")
        print(f"  Old: {sorted(list(old_n))}")
        print(f"  New: {sorted(list(new_n))}")
        added = new_n - old_n
        removed = old_n - new_n
        if added: print(f"  Added: {added}")
        if removed: print(f"  Removed: {removed}")
        diffs += 1

if diffs == 0:
    print("No differences in neighbor graph!")
