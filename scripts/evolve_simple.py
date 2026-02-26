import re

with open('make_map.py', 'r') as f: code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H, W = len(grid), max(len(r) for r in grid)
for i in range(H):
    grid[i].extend(['..'] * (W - len(grid[i])))

# Restoring the perfect original base grid manually
# First, revert to the base version (except IN/IL which we know are correct):
original_lines = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH MA MA",
    ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI MI NY NY NY MA CT MA MA MA RI",
    ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN IN OH OH PA PA NJ NY CT CT CT RI",
    ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA DE DE DE DE .. ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA MD MD DE DE .. ..",
    ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM NM OK OK OK MO MO KY KY VA VA VA VA MD MD .. .. .. ..",
    ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR TN MO TN TN TN NC VA NC NC NC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL GA GA GA SC SC SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA LA LA LA MS MS AL AL AL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .."
]

for r in range(H):
    row_words = original_lines[r].split()
    row_words.extend(['..'] * (W - len(row_words)))
    grid[r] = row_words

grid[6][20] = 'IN'; grid[6][19] = 'IL'

# Now we surgical-strike connect the blocks that are disconnected!
# 1. MO: R07[18] -> R08[19]. Let's make R08[18] = MO (it was KS).
grid[8][18] = 'MO'
# MO: R09[19] -> R10[21]. Let's make R10[20] = MO (it was TN). 
# Wait, if R10[20] = MO, then TN is split!
# So instead, let's make R10[21] = TN! Then MO doesn't go down to R10.
grid[10][21] = 'TN'
# But if MO doesn't go to R10, does it touch TN/AR? 
# MO is at R09[18,19]. TN is at R10[20..24]. AR is at R10[19].
# MO(19) touches AR(19) orthogonally! TN(20) touches MO(19) diagonally.
# Let's make R09[20] = TN so MO(19) touches TN(20) orthogonally!
grid[9][20] = 'TN' 
# R09[20] was KY. Now KY is only R09[21] and R08[21..23]. KY continuous!

# 2. VA: R09[25] -> R10[26].
# Make R10[25] = VA (was NC). But this splits NC!
# Just put VA at R10[26] into R09! R09[26] = VA (was MD).
grid[9][26] = 'VA'
grid[10][26] = 'NC' # replace the VA in R10 with NC!

# 3. NY: R04[25] -> R05[26]. Make R05[25] = NY (was NJ). 
# Then NJ is R05[24]? But R05[24] is PA!
# Let's just make R04[26] = NY. It was MA.
grid[4][26] = 'NY'
# Now MA is disconnected? MA was at R04[27], R03[30,31], R04[28..30].
# R03[30]=MA -> R04[28]=MA diagonally... We must connect MA!
# Let R03[29]=MA. It was NH. Let R03[28]=NH.
grid[3][29] = 'MA'
grid[4][27] = 'MA'

# 4. CT: R04[27] -> R05[28].
# Wait, R04[27] is MA. Original CT was R04[27].
# Let CT be R04[28], R05[28,29,30].
grid[4][28] = 'CT'
# R04[27] = MA. So MA connects to MA at R04[28..30]? But CT is at 28!
# Make MA R04[27], R03[29..31], and RI is R04[31].
grid[4][29] = 'MA'
grid[4][30] = 'MA'
# So CT is R05[28,29,30].
grid[4][28] = 'CT' # Let CT be 28 to touch MA.

# Let's write the whole top-right corner to be SAFE:
# R03: MI MI NY NY NY NY VT VT NH NH MA MA
grid[3][22:32] = ['NY', 'NY', 'NY', 'NY', 'VT', 'VT', 'NH', 'NH', 'MA', 'MA']
# R04: MI MI MI NY NY NY MA CT MA MA MA RI -> This splits MA!
# Let's write R04 to NOT split MA:
grid[4][22:32] = ['MI', 'NY', 'NY', 'NY', 'NY', 'MA', 'MA', 'MA', 'CT', 'RI']
# R05: IN IN OH OH PA PA NJ NY CT CT CT RI
grid[5][22:32] = ['OH', 'OH', 'PA', 'PA', 'NJ', 'NY', 'NY', 'CT', 'CT', 'RI']
# This fixes NY, MA, CT!

# 5. WV: R07[23] -> R08[24]. Make R08[23]=WV. (was KY)
grid[8][23] = 'WV'

# 6. KY: R07[20] -> R08[21]. Make R08[20]=KY. (was MO)
grid[8][20] = 'KY'

joined = ",\n    ".join('"' + " ".join(r) + '"' for r in grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]
with open('make_map.py', 'w') as f: f.write(new_code)
print("Finished safe evolution!")
