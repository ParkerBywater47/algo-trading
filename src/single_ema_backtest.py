import sys 
import time
import ema 

# these wouldn't be globals if Python supported constants
starting_capital = 450
fee_rate = .005


def main(): 
    """
    see usage function
    """
    has_header = True
    prices_csv = None
    verbose_output = False
    simulation = True

    # best performer
    periods_in_average = 5
    volatility_buffer = .075   

    # second best performer
#    periods_in_average = 13
#    volatility_buffer = 0.09   

    # a good performer over the 2020 dataset
    periods_in_average = 3
    volatility_buffer = .03

    # try to open the file 
    if len(sys.argv) < 2:
        print("Error: no data file given")
        usage()
        sys.exit(1)
    
    i = 2  
    while i < len(sys.argv): # have to do a while loop here because dumbass python 
        if sys.argv[i] == "-h":
            if i != len(sys.argv) -1: 
                if sys.argv[i + 1] == "f" or sys.argv[i + 1] == "false":
                    has_header = False 
                    i = i+1
                else:
                    print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                    sys.exit(1)
            else: 
                print("Error: Expected argument with '" + sys.argv[i] + "' option")
                sys.exit(1)
        elif sys.argv[i] == "-n":             
            if i != len(sys.argv) -1: 
                if sys.argv[i + 1].isdigit():
                    periods_in_average = int(sys.argv[i + 1])
                    i = i+1 
                else:
                    print("Error: Invalid arg '" + sys.argv[i+1] + "'")
                    sys.exit(1)
            else: 
                print("Error: Expected argument with '" + sys.argv[i] + "' option")
                sys.exit(1)
        elif sys.argv[i] == "-v": 
            verbose_output = True
        elif sys.argv[i] == "-s":             
            simulation = True 
        else: 
            print("Error: Invalid arg '" + sys.argv[i] + "'")
            sys.exit(1)
        i = i + 1
   
    price_data_idx = 2 
    price_data = []
    data_file = open(sys.argv[1])
    if has_header: 
        data_file.readline()
    for line in data_file:
        price_data.append(float(line.split(",")[price_data_idx]))

    best_performers = []
    for ema_length in range(1,50):
        for price_movement_threshold in range(5, 100):
            update_best(best_performers, \
                (ema_length, price_movement_threshold / 1000, ema.simulate(price_data, ema_length, price_movement_threshold / 1000, verbose_output=verbose_output, silent=True)))
    print(best_performers)


def update_best(a_list, current): 
    if len(a_list) < 6:
        a_list.append(current)
    else:
        mindx = 0 
        minimum = a_list[0][2]
        for i in range(1, len(a_list)):
            if a_list[i][2] < minimum: 
                mindx = i
                minimum = a_list[i][2]
            
        if current[2] > minimum: 
            a_list[mindx] = current


def average(lst): 
    the_sum = 0
    for i in lst:
        the_sum += i
    return the_sum / len(lst)


if __name__ == "__main__": 
    main()


