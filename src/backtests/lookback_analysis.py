f = open("data/lookback_10_bleh.txt")


loopback_length = 0
first_line = True
for line in f: 
    if line.startswith("s"): 
        loopback_length = int(line[line.find("length") + 6: line.find(",")].strip())
    else: 
        print(("\n" if not first_line else "") + line.strip() + ",", loopback_length, end="") 
        first_line = False

print()
f.close()
