import re

with open('make_map.py', 'r') as f: code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H, W = len(grid), max(len(r) for r in grid)
for i in range(H):
    grid[i].extend(['..'] * (W - len(grid[i])))

# R06: .. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA DE DE DE DE .. ..
grid[6][18] = 'MO'; grid[6][19] = 'IL'; grid[6][20] = 'IN'; grid[6][21] = 'OH'; grid[6][22] = 'OH'

# R07: .. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA MD MD DE DE .. ..
grid[7][16] = 'KS'; grid[7][17] = 'KS'; grid[7][18] = 'MO'; grid[7][19] = 'IL'; grid[7][20] = 'KY'; grid[7][21] = 'OH'; grid[7][22] = 'OH'; grid[7][23] = 'WV'; grid[7][24] = 'PA'; grid[7][25] = 'PA'; grid[7][26] = 'MD'; grid[7][27] = 'MD'; grid[7][28] = 'DE'; grid[7][29] = 'DE'

# R08: .. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..
grid[8][15] = 'CO'; grid[8][16] = 'KS'; grid[8][17] = 'KS'; grid[8][18] = 'MO'; grid[8][19] = 'MO'; grid[8][20] = 'KY'; grid[8][21] = 'KY'; grid[8][22] = 'KY'; grid[8][23] = 'KY'; grid[8][24] = 'WV'; grid[8][25] = 'WV'; grid[8][26] = 'MD'; grid[8][27] = 'MD'; grid[8][28] = 'MD'; grid[8][29] = '..'

# R09: .. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM NM OK OK OK MO MO KY KY VA VA VA VA MD MD .. .. .. ..
grid[9][16] = 'OK'; grid[9][17] = 'OK'; grid[9][18] = 'MO'; grid[9][19] = 'MO'; grid[9][20] = 'KY'; grid[9][21] = 'KY'; grid[9][22] = 'VA'; grid[9][23] = 'VA'; grid[9][24] = 'VA'; grid[9][25] = 'VA'; grid[9][26] = 'VA'; grid[9][27] = 'MD'; grid[9][28] = '..'; grid[9][29] = '..'

# R10: .. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR TN MO TN TN TN NC VA NC NC NC .. ..
grid[10][15] = 'TX'; grid[10][16] = 'TX'; grid[10][17] = 'OK'; grid[10][18] = 'OK'; grid[10][19] = 'MO'; grid[10][20] = 'TN'; grid[10][21] = 'TN'; grid[10][22] = 'TN'; grid[10][23] = 'TN'; grid[10][24] = 'TN'; grid[10][25] = 'NC'; grid[10][26] = 'NC'; grid[10][27] = 'NC'; grid[10][28] = 'NC'; grid[10][29] = 'NC'; grid[10][30] = '..'

# R11: .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL GA GA GA SC SC SC .. ..
grid[11][15] = 'TX'; grid[11][16] = 'TX'; grid[11][17] = 'TX'; grid[11][18] = 'AR'; grid[11][19] = 'AR'; grid[11][20] = 'AR'; grid[11][21] = 'MS'; grid[11][22] = 'MS'; grid[11][23] = 'AL'; grid[11][24] = 'GA'; grid[11][25] = 'GA'; grid[11][26] = 'GA'; grid[11][27] = 'SC'; grid[11][28] = 'SC'; grid[11][29] = 'SC'; grid[11][30] = '..'

# Let's double-check AR neighbors. AR touches TX, OK, MO, TN, MS, LA.
# AR is at R11[18,19,20].
# OK is at R10[17,18]. AR(18) touches OK(18).
# TX is at R11[16,17], R10[15,16]. AR(18) touches TX(17).
# MO is at R10[19]. AR(19) touches MO(19).
# TN is at R10[20..24]. AR(20) touches TN(20).
# MS is at R11[21,22]. AR(20) touches MS(21).
# LA is at R12. Does R12 have LA?
# R12 original: TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC
# AR(18) touches LA? Let's check R12.

grid[12][15] = 'TX'; grid[12][16] = 'TX'; grid[12][17] = 'TX'; grid[12][18] = 'TX'; grid[12][19] = 'LA'; grid[12][20] = 'LA'; grid[12][21] = 'MS'; grid[12][22] = 'MS'; grid[12][23] = 'AL'; grid[12][24] = 'AL'

# Does AR(18) touch LA(19)? Actually AR(18) touches TX(18) on R12. AR(19) touches LA(19). Yes!

joined = ",\n    ".join('"' + " ".join(r) + '"' for r in grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]

with open('make_map.py', 'w') as f:
    f.write(new_code)
print("Manually patched MO, VA, TN, KY, AR regions!")
