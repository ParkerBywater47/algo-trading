import sys
import ema
import sma


def main(): 
    if len(sys.argv) < 3: 
        print("Error: Must specify backtest and data file") 
    else:
        has_header = True
        silent = False
        verbose_output = False
        price_data_idx = 2
        
        i = 1 
        while i < len(sys.argv) - 2:
            arg = sys.argv[i]
            if arg == "-s":
                silent = True 
            elif arg == "-n": 
                has_header = False
            elif arg == "-v":  
                verbose_output = True
            elif arg == "-i": 
                if i + 1 < len(sys.argv) - 2: 
                    try: 
                        price_data_idx = int(sys.argv[i + 1]) 
                        i += 1
                        continue
                    except NumberFormatException:
                        pass
                print("Error: must specify integer with -i arg")
                sys.exit(1)
            else:
                print(f"Error: invalid argument '{arg}'")
                sys.exit(1)
            i = i + 1
        
        algo = sys.argv[len(sys.argv) - 2]     

        price_data = []
        with open(sys.argv[len(sys.argv) - 1]) as prices_file: 
            if has_header: 
                prices_file.readline()
            for line in prices_file: 
                price_data.append(float(line.split(",")[price_data_idx])) 
       
        if algo == "ema": 
            ema.simulate(price_data, verbose_output=verbose_output, silent=silent)
        elif algo == "sma": 
            sma.simulate(price_data, verbose_output=verbose_output, silent=silent)
#        elif algo == "macd": 
#            macd.simulate(price_data, verbose_output=verbose_output, silent=silent) 
#        elif algo == "double_sma": 
#            double_sma.simulate(price_data, verbose_output=verbose_output, silent=silent)
        else:
            print(f"Error: algorithm '{algo}' not installed")


if __name__ == "__main__": 
    main()
