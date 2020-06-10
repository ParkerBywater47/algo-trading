#include <iostream>
#include <fstream> 
#include <string>
#include <vector>
#include <list> 
#include <cstdlib>
//#include <omp.h>

using namespace std;

struct ResultStruct { 
    int ema_length;
    double price_movement_threshold; 
    double performance_metric;
}; 

void find_optimal_dynema(const vector<double> hist_data, const vector<double> price_data, double* result_table[]); 
double simulate_dynamic_ema(const vector<double> hist_data, const vector<double> price_data, const int readjustment_time, const int lookback_length, const double starting_capital, const double fee_rate)  ; 
double simulate_ema(const vector<double> hist_data, const vector<double> price_data, const double ema_length, const double price_movement_threshold, const double starting_capital, const double fee_rate); 
ResultStruct find_optimal_ema(const vector<double> hist_data, const vector<double>price_data, const double starting_capital, const double fee_rate);
inline vector<double> list_to_vec(list<double> the_list);

const static int MAX_READJUSTMENT_TIME = 36; 
const static int MIN_READJUSTMENT_TIME = 7;
const static int MAX_LOOKBACK_LENGTH = 140;
const static int MIN_LOOKBACK_LENGTH = 60;
const static int MAX_EMA_LENGTH = 50; 
const static double STARTING_CAPITAL = 450.0; 
const static double TX_FEE_RATE = 0.0;

void find_optimal_dynema(const vector<double> hist_data, const vector<double> price_data, double* result_table[]) { 
    # pragma omp parallel 
    # pragma omp for
    for (int i = MIN_READJUSTMENT_TIME; i <= MAX_READJUSTMENT_TIME; i++) { 
        for (int j = MIN_LOOKBACK_LENGTH; j <= MAX_LOOKBACK_LENGTH; j++) {
//            cout << "simulating " << i << ", " << j << endl; 
            result_table[i - MIN_READJUSTMENT_TIME][j - MIN_LOOKBACK_LENGTH] = simulate_dynamic_ema(hist_data, price_data, i, j, STARTING_CAPITAL, TX_FEE_RATE);
//            cout << "this shouldn't be wEiRd: " << val << endl ;
            //cout << "why tf is this weird val " << result_table[i - MIN_READJUSTMENT_TIME][j - MIN_LOOKBACK_LENGTH] << endl ; 
        }
    }
} 


double simulate_dynamic_ema(const vector<double> hist_data, const vector<double> price_data, const int readjustment_time, const int lookback_length, const double starting_capital, const double fee_rate) { 
//   if not silent: 
//       print("simulating dynamic ema with lookback length " + str(lookback_length) + ", fee rate " + format(fee_rate, ".2%"))

    list<double> hist_days_for_ema;
    for (size_t i = hist_data.size() - lookback_length - MAX_EMA_LENGTH - 1; i < hist_data.size() - lookback_length; i++) {
        hist_days_for_ema.push_back(hist_data[i]);
    }
    
    cout << "last 5 elements of hist_days_for_ema" << endl;
    for (size_t i = list_to_vec(hist_days_for_ema).size() - 5; i < list_to_vec(hist_days_for_ema).size(); i++) { 
        cout << list_to_vec(hist_days_for_ema)[i] << ", ";
    }
    cout << endl;

    list<double> lookback_days;
    for (size_t i = hist_data.size() - lookback_length; i < hist_data.size(); i++) { 
        lookback_days.push_back(hist_data[i]);
    }
    cout << "last 5 elements of lookback_days" << endl;
    for (size_t i = list_to_vec(lookback_days).size() - 5; i < list_to_vec(lookback_days).size(); i++) { 
        cout << list_to_vec(lookback_days)[i] << ", ";
    }
    cout << endl;
  

//    cout << "size of hist_days_for_ema in simulate_dynamic_ema: " << hist_days_for_ema.size() << endl;
//    cout << "size of lookback days in simulate_dynamic_ema: " << lookback_days.size() << endl;
//    exit(0);
    ResultStruct optimal_ema = find_optimal_ema(list_to_vec(hist_days_for_ema), list_to_vec(lookback_days), starting_capital, fee_rate); 
    int ema_length = optimal_ema.ema_length;
    double price_movement_threshold = optimal_ema.price_movement_threshold; 
    
//    cout << "best ema at start: " << ema_length << ", " << price_movement_threshold << endl; 

    // compute an sma to start
    double sum_for_avg = 0; 
    size_t j; 
    int els = 0; 
    for (j = hist_data.size() - ema_length - 1; j < hist_data.size() - 1; j++)  // I'm pretty sure this will give me the correct number of elements for computing the initial sma
    { 
        sum_for_avg += hist_data[j]; 
        ++els;
    } 
//    cout << "ema_length: " << ema_length << endl;  
//    cout << "els included in sma: " << els << endl;
//    exit(0); 
    double sma = sum_for_avg / ema_length; 
    int smoothing_factor = 2; 
    double multiplier = smoothing_factor / (ema_length + 1); 
    double start_day_price = price_data[j + 1]; 
    double ema = start_day_price * multiplier + sma * (1 - multiplier); 
//    print("initial ema:", ema)
//    print("multiplier:", multiplier)
//    print("sma:", sma)
//    print("start:", start_day_price)
        

    double coins_owned = 0;
    double cash_money = starting_capital;
    bool bought = false;
    double today_price = price_data[0]; 
    double max_purchase_amt = cash_money / (1 + fee_rate); 
    double initial_coin_purchase = max_purchase_amt / today_price;
    int days_since_update = 0; 
    for (size_t i = 0; i < price_data.size(); i++) { 
//        print(ema_length, price_movement_threshold)
        today_price = price_data[i]; 
        
        double signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold)); 
//        if verbose_output:
//            print("today: " + format(today_price, "<10.2f")  + "signal price: "  + format(signal_price, ".2f"))
//            print("cash: " + str(cash_money) + "    " + "shares owned: " + str(coins_owned))

        if (bought == false && today_price > signal_price) { 
            bought = true;   
            max_purchase_amt = cash_money / (1 + fee_rate); 
            cash_money = 0; 
            coins_owned += max_purchase_amt / today_price; 
//           if verbose_output:
//               print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
        } 
        else if (bought == true && today_price < signal_price) { 
            bought = false; 
            cash_money += (coins_owned * today_price) / (1 + fee_rate); 
//           if verbose_output 
//               print("sold " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
            coins_owned = 0; 
        }
         
        hist_days_for_ema.push_back(lookback_days.front());
        hist_days_for_ema.pop_front();
        lookback_days.push_back(today_price); 
        lookback_days.pop_front(); 

//        if (i %100 == 0) { 
//        cout << "last 5 elements of hist_days_for_ema" << endl;
//        for (size_t k = list_to_vec(hist_days_for_ema).size() - 5; k < list_to_vec(hist_days_for_ema).size(); k++) { 
//            cout << list_to_vec(hist_days_for_ema)[k] << ", ";
//        }
//        cout << endl;
//        }
//        exit(0); 

        
        if (days_since_update % readjustment_time == 0) {
            ema_length = find_optimal_ema(list_to_vec(hist_days_for_ema), list_to_vec(lookback_days), starting_capital, fee_rate).ema_length;  
            //cout << "updated ema_length to " << ema_length << endl; 
        } 
        
        multiplier = smoothing_factor / (ema_length + 1); 

        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier);  
        ++days_since_update;
    }
 
    if (bought) { 
        cash_money += (coins_owned * today_price) / (1 + fee_rate) ;
    } 
    
    double algo_returns = (cash_money - starting_capital) / starting_capital;
    double market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital; 
//    if not silent:
//        print("algo: " + format(algo_returns, ".2%"))
//        print("market: " + format(market_returns, ".2%"))

    return algo_returns - market_returns;
}


ResultStruct find_optimal_ema(const vector<double> hist_data, const vector<double> price_data, const double starting_capital, const double fee_rate) { 
    ResultStruct best_performer{-1, -1, -100000.0}; 
    for (int ema_length = 1; ema_length <= MAX_EMA_LENGTH; ema_length++) 
    { 
        for (int price_movement_threshold = 5; price_movement_threshold <= 100; price_movement_threshold++)
        {
            double this_run = simulate_ema(hist_data, price_data, ema_length, price_movement_threshold / 1000.0, starting_capital, fee_rate);  
//            cout << "performanc of " << ema_length << ", " << price_movement_threshold / 1000.0 << " ema: " << this_run << endl;
            best_performer = best_performer.performance_metric > this_run ? best_performer : ResultStruct{ema_length, price_movement_threshold / 1000.0, this_run};
            //cout << "best_performer: " << best_performer.ema_length << ", " << best_performer.price_movement_threshold << ", " << best_performer.performance_metric <<  endl;
        } 
    }
    return best_performer;
}


double simulate_ema(const vector<double> hist_data, const vector<double> price_data, const double ema_length, const double price_movement_threshold, const double starting_capital, const double fee_rate) { 
    // compute an sma to start
    double sum_for_avg = 0;  
    size_t j; 
    vector<double>::const_iterator it = hist_data.end() - ema_length - 1; 
    for (j = hist_data.size() - ema_length -1; j < hist_data.size() - 1; j++, it++) 
    { 
        sum_for_avg += hist_data[j];
    }
    cout << "in simulate_ema: " <<  hist_data[j] << endl; 
    cout << "in simulate_ema: " <<  *it << endl; 
    double sma = sum_for_avg / ema_length; 
    const int smoothing_factor = 2; 
    int multiplier = smoothing_factor / (ema_length + 1); 
    double start_day_price = hist_data[j + 1]; 
    double ema = start_day_price * multiplier + sma * (1 - multiplier); 
//    print("initial ema:", ema)
//    print("multiplier:", multiplier)
//    print("sma:", sma)
//    print("start:", start_day_price)
        
    double coins_owned = 0; 
    double cash_money = starting_capital; 
    bool bought = false; 
    double today_price = price_data[0]; 
    double max_purchase_amt = cash_money / (1 + fee_rate); 
    double initial_coin_purchase = max_purchase_amt / price_data[0]; 
    for (size_t i = 0; i < price_data.size(); i++) // swap this out with an iterator like a big boy some day 
    {   
        today_price = price_data[i]; 
        double signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold)); 
//       if verbose_output { 
//           print("today: " + format(today_price, "<10.2f")  + "signal price: "  + format(signal_price, ".2f"))
//           print("cash: " + str(cash_money) + "    " + "coins owned: " + str(coins_owned)) } 

        if (bought == false && today_price > signal_price) { 
            bought = true;   
            max_purchase_amt = cash_money / (1 + fee_rate); 
            cash_money = 0; 
            coins_owned += max_purchase_amt / today_price; 
//           if verbose_output:
//               print("bought " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
        } 

        else if (bought == true && today_price < signal_price) { 
            bought = false; 
            cash_money += (coins_owned * today_price) / (1 + fee_rate); 
//           if verbose_output 
//               print("sold " + format(coins_owned, ".5f") + " at " + format(today_price, ".2f"))
            coins_owned = 0; 
        }

        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier); 
    }
 
    if (bought) {
        cash_money += (coins_owned * today_price) / (1 + fee_rate); 
    }
    
    double algo_returns = (cash_money - starting_capital) / starting_capital; 
    double market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital; 
     
//   if not silent:
//       print("algo: " + format(algo_returns, ".2%"))
//       print("market: " + format(market_returns, ".2%"))

    return algo_returns - market_returns; 
}


int main(int argc, char* args[]) { 

    if (argc <= 2) {
        cout << "must enter history and simulation data files" << endl;
        return 1;    
    }

    // read data files    
    ifstream historic_data_file(args[1], fstream::in); 
    ifstream sim_data_file(args[2], fstream::in);
    string line;
    vector<double> hist_data; 
    // discard header
    getline(historic_data_file,line); 
    while ( getline(historic_data_file,line) ) { hist_data.push_back(stof(line)); }
    vector<double> sim_data; 
    // discard header
    getline(sim_data_file,line); 
    while ( getline(sim_data_file,line) ) { sim_data.push_back(stof(line)); }

    // make a table for results
    double ** results = new double*[MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1]; 
    for (int i = 0; i < MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1; i++) { 
        results[i] = new double[MAX_LOOKBACK_LENGTH - MIN_LOOKBACK_LENGTH + 1]; }

    // simulate and report results
    find_optimal_dynema(hist_data, sim_data, results);
    for (int i = 0; i < MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1; i++) { 
        for (int j = 0; j < MAX_LOOKBACK_LENGTH - MIN_LOOKBACK_LENGTH + 1; j++) {  
            cout << results[i][j] << ", " << i + MIN_READJUSTMENT_TIME << ", " << j + MIN_LOOKBACK_LENGTH << endl;  
        }    
    } 
    
    for (int i = 0; i < MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1; i++) { 
        delete[] results[i]; }
    delete[] results; 

    historic_data_file.close();
    sim_data_file.close();
    return 0; 
}


vector<double> list_to_vec(list<double> the_list) { 
    vector<double> out(the_list.size());
    int i = 0; 
    for (list<double>::iterator it = the_list.begin(); it != the_list.end(); ++it) { 
//        cout << "value pointed to by list iterator in list_to_vec: " << *it << endl;
        out[i++] = *it; 
    }
    return out; 
}
