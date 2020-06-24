import sys

was_better_times = 0
total_times = 0
with open(sys.argv[1]) as f: 
    while True:
        if f.readline() == "":
            break
    
        algo_line = f.readline()
        market_line = f.readline()

        if float(algo_line.strip()[5:-1]) > float(market_line.strip()[7:-1]):
            was_better_times += 1
        total_times += 1

print(was_better_times, total_times)

