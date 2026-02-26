r8 = ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO CO KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..".split()
r9 = ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM UT OK OK MO AR MO KY KY VA VA VA VA MD MD .. .. .. ..".split()
r10= ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR AR TN TN TN TN TN NC NC NC NC .. ..".split()
lines = [r8, r9, r10]
for y in range(3):
    for x in range(len(lines[y])):
        if lines[y][x] == 'NM':
            print(f"NM at {y}, {x}. Neighbors: up={lines[y-1][x] if y>0 else '.'}, down={lines[y+1][x] if y<2 else '.'}, left={lines[y][x-1]}, right={lines[y][x+1]}")
