
sc_anon_cost = 150
sc_file_cost = 300
swappiness = 100

total_cost = sc_anon_cost + sc_file_cost
anon_cost = total_cost + sc_anon_cost
file_cost = total_cost + sc_file_cost
total_cost = anon_cost + file_cost

ap = swappiness * (total_cost + 1)
ap = ap / (anon_cost + 1)

fp = (200 - swappiness) * (total_cost + 1)
fp = fp / (file_cost + 1)
denomiantor = ap + fp

anon_frac = ap/denomiantor
file_frac = fp/denomiantor
scan = 1000

print("sc_anon_cost:", sc_anon_cost)
print("sc_file_cost:", sc_file_cost)
print("swappiness:", swappiness)
print("anon_cost:", anon_cost)
print("file_cost:", file_cost)
print("total_cost:", total_cost)
print("ap:", ap)
print("fp:", fp)

print("anon_frac:", anon_frac)
print("file_frac:", file_frac)
# print(scan)
