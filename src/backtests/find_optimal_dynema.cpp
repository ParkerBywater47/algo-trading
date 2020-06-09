#include <iostream>
#include <fstream> 
#include <string>
#include <vector>
#include <list> 
#include <cstdlib>
#include <omp.h>

using namespace std;

struct ResultStruct { 
    int ema_length;
    double price_movement_threshold; 
    float performance_metric;
}; 

void find_optimal_dynema(const vector<float> hist_data, const vector<float> price_data, float* result_table[]); 
float simulate_dynamic_ema(const vector<float> hist_data, const vector<float> price_data, const int readjustment_time, const int lookback_length, const float starting_capital, const float fee_rate)  ; 
float simulate_ema(const vector<float> hist_data, const vector<float> price_data, const float ema_length, const float price_movement_threshold, const float starting_capital, const float fee_rate); 
ResultStruct find_optimal_ema(const vector<float> hist_data, const vector<float>price_data, const float starting_capital, const float fee_rate);
inline vector<float> list_to_vec(list<float> the_list);

const int MAX_READJUSTMENT_TIME = 36; 
const int MIN_READJUSTMENT_TIME = 7;
const int MAX_LOOKBACK_LENGTH = 140;
const int MIN_LOOKBACK_LENGTH = 60;
const int MAX_EMA_LENGTH = 50; 
const float STARTING_CAPITAL = 450.0; 
const float TX_FEE_RATE = 0.0;

void find_optimal_dynema(const vector<float> hist_data, const vector<float> price_data, float* result_table[]) { 
    # pragma omp parallel
    # pragma omp for
    for (int i = MIN_READJUSTMENT_TIME; i <= MAX_READJUSTMENT_TIME; i++) { 
        for (int j = MIN_LOOKBACK_LENGTH; j <= MAX_LOOKBACK_LENGTH; j++) {
            cout << "simulating " << i << ", " << j << endl; 
            float val = simulate_dynamic_ema(hist_data, price_data, i, j, STARTING_CAPITAL, TX_FEE_RATE);
//            result_table[i - MIN_READJUSTMENT_TIME][j - MIN_LOOKBACK_LENGTH] = val; //simulate_dynamic_ema(hist_data, price_data, i, j, STARTING_CAPITAL, TX_FEE_RATE);
            cout << "this shouldn't be wEiRd: " << val << endl ;
//            cout << "why tf is this weird val " << result_table[i - MIN_READJUSTMENT_TIME][j - MIN_LOOKBACK_LENGTH]; 
        }
    }
} 


float simulate_dynamic_ema(const vector<float> hist_data, const vector<float> price_data, const int readjustment_time, const int lookback_length, const float starting_capital, const float fee_rate) { 
//   if not silent: 
//       print("simulating dynamic ema with lookback length " + str(lookback_length) + ", fee rate " + format(fee_rate, ".2%"))

    list<float> hist_days_for_ema;
    for (size_t i = hist_data.size() - lookback_length - MAX_EMA_LENGTH - 1; i < hist_data.size() - lookback_length; i++) {
        hist_days_for_ema.push_back(hist_data[i]);
    }
    
//    cout << "last 5 elements of hist_days_for_ema" << endl;
//    for (size_t i = list_to_vec(hist_days_for_ema).size() - 5; i < list_to_vec(hist_days_for_ema).size(); i++) { 
//        cout << list_to_vec(hist_days_for_ema)[i] << ", ";
//    }
//    cout << endl;

    list<float> lookback_days;
    for (size_t i = hist_data.size() - lookback_length; i < hist_data.size(); i++) { 
        lookback_days.push_back(hist_data[i]);
    }
//    cout << "last 5 elements of lookback_days" << endl;
//    for (size_t i = list_to_vec(lookback_days).size() - 5; i < list_to_vec(lookback_days).size(); i++) { 
//        cout << list_to_vec(lookback_days)[i] << ", ";
//    }
//    cout << endl;

//    cout << "size of hist_days_for_ema in simulate_dynamic_ema: " << hist_days_for_ema.size() << endl;
//    cout << "size of lookback days in simulate_dynamic_ema: " << lookback_days.size() << endl;
//    exit(0);
    ResultStruct optimal_ema = find_optimal_ema(list_to_vec(hist_days_for_ema), list_to_vec(lookback_days), starting_capital, fee_rate); 
    int ema_length = optimal_ema.ema_length;
    float price_movement_threshold = optimal_ema.performance_metric; 

    // compute an sma to start
    float sum_for_avg = 0; 
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
    float sma = sum_for_avg / ema_length; 
    int smoothing_factor = 2; 
    float multiplier = smoothing_factor / (ema_length + 1); 
    float start_day_price = price_data[j + 1]; 
    float ema = start_day_price * multiplier + sma * (1 - multiplier); 
//    print("initial ema:", ema)
//    print("multiplier:", multiplier)
//    print("sma:", sma)
//    print("start:", start_day_price)
        

    float coins_owned = 0;
    float cash_money = starting_capital;
    bool bought = false;
    float today_price; 
    float max_purchase_amt = cash_money / (1 + fee_rate); 
    float initial_coin_purchase = max_purchase_amt / today_price ;
    int days_since_update = 0; 
    for (size_t i = 0; i < price_data.size(); i++) { 
//        print(ema_length, price_movement_threshold)
        today_price = price_data[i]; 
        
        float signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold)); 
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

//        cout << "last 5 elements of hist_days_for_ema" << endl;
//        for (size_t i = list_to_vec(hist_days_for_ema).size() - 5; i < list_to_vec(hist_days_for_ema).size(); i++) { 
//            cout << list_to_vec(hist_days_for_ema)[i] << ", ";
//        }
//        cout << endl;
//        exit(0); 

        
        if (days_since_update % readjustment_time == 0) {
            ema_length = find_optimal_ema(list_to_vec(hist_days_for_ema), list_to_vec(lookback_days), starting_capital, fee_rate).ema_length;  // God, please remember to change this
        } 
        
        multiplier = smoothing_factor / (ema_length + 1); 

        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier);  
        ++days_since_update;
    }
 
    if (bought) { 
        cash_money += (coins_owned * today_price) / (1 + fee_rate) ;
    } 
    
    float algo_returns = (cash_money - starting_capital) / starting_capital;
    float market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital; 
   
//    if not silent:
//        print("algo: " + format(algo_returns, ".2%"))
//        print("market: " + format(market_returns, ".2%"))

//    print(format(algo_returns - market_returns, ".2%") + ", " + ("+" if algo_returns > 0 else "-"))
    return algo_returns - market_returns;
}


ResultStruct find_optimal_ema(const vector<float> hist_data, const vector<float> price_data, const float starting_capital, const float fee_rate) { 
    ResultStruct best_performer{-1, -1, -100000.0}; 
    for (int ema_length = 1; ema_length <= MAX_EMA_LENGTH; ema_length++) 
    { 
        for (int price_movement_threshold = 5; price_movement_threshold <= 100; price_movement_threshold++)
        {
            float this_run = simulate_ema(hist_data, price_data, ema_length, price_movement_threshold / 1000.0, starting_capital, fee_rate);  
            best_performer = best_performer.performance_metric > this_run ? best_performer : ResultStruct{ema_length, price_movement_threshold / 1000.0, this_run};
        } 
    }
    return best_performer;
}


float simulate_ema(const vector<float> hist_data, const vector<float> price_data, const float ema_length, const float price_movement_threshold, const float starting_capital, const float fee_rate) { 
    // compute an sma to start
    float sum_for_avg = 0;  
    size_t j; 
    for (j = hist_data.size() - ema_length -1; j < hist_data.size() - 1; j++) // remember to verify that this for loop actually reads the right amount of data
    { 
        sum_for_avg += hist_data[j];
    }
    float sma = sum_for_avg / ema_length; 
    const int smoothing_factor = 2; 
    int multiplier = smoothing_factor / (ema_length + 1); 
    float start_day_price = hist_data[j + 1]; 
    float ema = start_day_price * multiplier + sma * (1 - multiplier); 
//    print("initial ema:", ema)
//    print("multiplier:", multiplier)
//    print("sma:", sma)
//    print("start:", start_day_price)
        
    float coins_owned = 0; 
    float cash_money = starting_capital; 
    bool bought = false; 
    float today_price; 
    float max_purchase_amt = cash_money / (1 + fee_rate); 
    float initial_coin_purchase = max_purchase_amt / price_data[0]; 
    for (size_t i = 0; i < price_data.size(); i++) // swap this out with an iterator like a big boy some day 
    {   
        today_price = price_data[i]; 
        float signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold)); 
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
    
    float algo_returns = (cash_money - starting_capital) / starting_capital; 
    float market_returns = (initial_coin_purchase * today_price / (1 + fee_rate) - starting_capital) / starting_capital; 
    
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
    vector<float> hist_data; 
    // discard header
    getline(historic_data_file,line); 
    while ( getline(historic_data_file,line) ) { hist_data.push_back(stof(line)); }
    vector<float> sim_data; 
    // discard header
    getline(sim_data_file,line); 
    while ( getline(sim_data_file,line) ) { sim_data.push_back(stof(line)); }

    // make a table for results
    float ** results = new float*[MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1]; 
    for (int i = 0; i < MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1; i++) { 
        results[i] = new float[MAX_LOOKBACK_LENGTH - MIN_LOOKBACK_LENGTH + 1]; }

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


inline vector<float> list_to_vec(list<float> the_list) { 
    vector<float> out(the_list.size());
    int i = 0; 
    for (list<float>::iterator it = the_list.begin(); it != the_list.end(); ++it) { 
        out[i++] = *it; 
    }
    return out; 
}
