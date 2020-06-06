import dynamic_ema    
import operator
import find_optimal_ema

    
def optimize(price_data, fee_rate, verbose_output, silent):
    best_performers = []
    for i in range(80, 100):
        find_optimal_ema.update_best(best_performers, (20, i, dynamic_ema.simulate(price_data, lookback_length=i, fee_rate=fee_rate, verbose_output=verbose_output, silent=True)))
    best_performers = sorted(best_performers, key=operator.itemgetter(2)) 
    if not silent:
        print(best_performers)
    return best_performers
