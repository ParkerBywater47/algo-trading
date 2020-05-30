#!/usr/bin/python3
import sys
import ema
import sma
import macd
import double_sma
import find_optimal_ema


def main(): 
    if len(sys.argv) < 3: 
        print("Error: Must specify trade algorithm and data file") 
    else:
        has_header = True
        silent = False
        verbose_output = False
        price_data_idx = 2
        algo = sys.argv[1]
        fee_rate = .005
        
        i = 2 
        while i < len(sys.argv) - 1:
            arg = sys.argv[i]
            if arg == "-s" or arg == "--silent":
                silent = True 
            elif arg == "-n" or arg == "--no-header": 
                has_header = False
            elif arg == "-v" or arg == "--verbose":  
                verbose_output = True
            elif arg == "-d" or arg == "--data-index": 
                try: 
                    price_data_idx = int(sys.argv[i + 1]) 
                    i += 1
                except ValueError:
                    print("Error: must specify integer with -d arg")
                    sys.exit(1)
                except IndexError:
                    print("Error: must specify integer with -d arg")
                    sys.exit(1)
            elif arg == "-f" or arg == "--fee-rate": 
                try: 
                    fee_rate = float(sys.argv[i + 1]) 
                    i += 1
                except ValueError:
                    print("Error: must specify float with -f arg")
                    sys.exit(1)
                except IndexError:
                    print("Error: must specify float with -f arg")
                    sys.exit(1)
            else:
                print(f"Error: invalid argument '{arg}'")
                sys.exit(1)
            i = i + 1

        price_data = []
        with open(sys.argv[len(sys.argv) - 1]) as prices_file: 
            if has_header: 
                prices_file.readline()
            for line in prices_file: 
                price_data.append(float(line.split(",")[price_data_idx])) 
       
        if algo == "ema": 
            ema.simulate(price_data, fee_rate=fee_rate, verbose_output=verbose_output, silent=silent)
        elif algo == "sma": 
            sma.simulate(price_data, fee_rate=fee_rate, verbose_output=verbose_output, silent=silent)
#        elif algo == "macd": 
#            macd.simulate(price_data, verbose_output=verbose_output, silent=silent) 
        elif algo == "dsma": 
            double_sma.simulate(price_data, 50, 200, verbose_output=verbose_output, silent=silent)
        elif algo == "foe": # 
            find_optimal_ema.optimize(price_data, fee_rate=fee_rate, verbose_output=verbose_output, silent=silent)
        else:
            print(f"Error: algorithm '{algo}' not installed")


if __name__ == "__main__": 
    main()
