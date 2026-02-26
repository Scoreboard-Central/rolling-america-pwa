# This script encodes the exact neighbors and colors from visual inspection of the image

image_colors = {
    'WA': 'orange', 'OR': 'orange', 'CA': 'orange', 'NV': 'orange', 'UT': 'orange', 'AZ': 'orange', 'ID': 'orange', 'AK': 'orange', 'HI': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'MI': 'blue', 'IN': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green',
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'MS': 'yellow', 'TN': 'yellow', 'AL': 'yellow', 'KY': 'yellow', 'FL': 'yellow',
    'PA': 'red', 'OH': 'red', 'WV': 'red', 'VA': 'red', 'NC': 'red', 'SC': 'red', 'GA': 'red', 'MD': 'red', 'DE': 'red',
    'NY': 'purple', 'NJ': 'purple', 'CT': 'purple', 'RI': 'purple', 'MA': 'purple', 'VT': 'purple', 'NH': 'purple', 'ME': 'purple'
}

# Encode all neighbors I can see in the image
edges = [
    # West Coast
    ('WA', 'OR'), ('WA', 'MT'), ('WA', 'ID'), # Wait, does WA touch ID? In visual WA touches MT directly.
]

# Let's count colors just to verify 8, 9, 7, 8, 9, 8 = 49 states
counts = {}
for s, c in image_colors.items():
    counts[c] = counts.get(c, 0) + 1
print("Color counts:", counts)
