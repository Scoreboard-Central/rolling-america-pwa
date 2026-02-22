import re

target_colors = {
    'AK': 'ra-orange', 'HI': 'ra-orange', 'WA': 'ra-orange', 'OR': 'ra-orange',
    'CA': 'ra-orange', 'NV': 'ra-orange', 'ID': 'ra-orange', 'UT': 'ra-orange', 'AZ': 'ra-orange',
    'MT': 'ra-blue', 'WY': 'ra-blue', 'ND': 'ra-blue', 'SD': 'ra-blue',
    'NE': 'ra-blue', 'MN': 'ra-blue', 'IA': 'ra-blue', 'WI': 'ra-blue', 'CO': 'ra-blue',
    'NM': 'ra-green', 'KS': 'ra-green', 'OK': 'ra-green',
    'TX': 'ra-green', 'MO': 'ra-green', 'AR': 'ra-green', 'LA': 'ra-green',
    'IL': 'ra-yellow', 'MI': 'ra-yellow', 'IN': 'ra-yellow',
    'OH': 'ra-yellow', 'KY': 'ra-yellow', 'TN': 'ra-yellow', 'MS': 'ra-yellow', 'AL': 'ra-yellow',
    'GA': 'ra-red', 'FL': 'ra-red', 'SC': 'ra-red', 'NC': 'ra-red', 
    'VA': 'ra-red', 'WV': 'ra-red', 'PA': 'ra-red', 'MD': 'ra-red', 'DE': 'ra-red',
    'NJ': 'ra-purple', 'NY': 'ra-purple', 'CT': 'ra-purple', 'RI': 'ra-purple', 'MA': 'ra-purple',
    'VT': 'ra-purple', 'NH': 'ra-purple', 'ME': 'ra-purple'
}

hex_colors = {
    'ra-orange': '#F4B384', 'ra-blue': '#85BBEA', 'ra-green': '#9ACC99',
    'ra-yellow': '#F4D075', 'ra-red': '#F29C9C', 'ra-purple': '#A4A6D5'
}

with open('src/app/app.component.html', 'r') as f:
    text = f.read()

for state, cname in target_colors.items():
    color = hex_colors[cname]
    start_tag = f"(click)=\"openModal('state', '{state}')\">"
    s_idx = text.find(start_tag)
    if s_idx == -1: continue
    e_idx = text.find('</g>', s_idx)
    block = text[s_idx:e_idx]
    
    # replace all fill="..." in this block
    new_block = re.sub(r'fill="#[A-Fa-f0-9]+"', f'fill="{color}"', block)
    text = text[:s_idx] + new_block + text[e_idx:]

with open('src/app/app.component.html', 'w') as f:
    f.write(text)

# Also update generate_map.py
with open('scripts/generate_map.py', 'r') as f:
    gen_text = f.read()

dict_str = "colors = {\n"
for cname in ['ra-orange', 'ra-blue', 'ra-green', 'ra-yellow', 'ra-red', 'ra-purple']:
    states = [s for s, c in target_colors.items() if c == cname]
    dict_str += f"    {', '.join(repr(s)+': '+repr(cname) for s in states)},\n"
dict_str += "}"

start_dict = gen_text.find('colors = {')
end_dict = gen_text.find('}', start_dict) + 1
gen_text = gen_text[:start_dict] + dict_str + gen_text[end_dict:]

with open('scripts/generate_map.py', 'w') as f:
    f.write(gen_text)

print("Updated perfectly")
