#include <iostream>
#include <fstream> 
#include <string>
#include <cstdlib>
#include <omp.h>

using namespace std;

struct ResultStruct { 
    int ema_length;
    double price_movement_threshold; 
    double performance_metric;
}; 

void find_optimal_dynema(const float price_data[], const int start_day_idx, double* result_table[], const int price_data_size); 
double simulate_dynamic_ema(const float price_data[], const int start_day_idx, const int readjustment_time, const int lookback_length, const int price_data_size); 
ResultStruct find_optimal_ema(const float price_data[], const int start_day_idx, const int last_day_idx, const int price_data_size); 
double simulate_ema(const float price_data[], const int start_day_idx, const int last_day_idx, const int ema_length, const double price_movement_threshold, const int price_data_size);
//double simulate_ema(const float price_data[], const int start_day_idx, const int last_day_idx, const int ema_length, const double price_movement_threshold, const int price_data_size, bool print);

const static int MAX_READJUSTMENT_TIME = 36; 
const static int MIN_READJUSTMENT_TIME = 7;
const static int MAX_LOOKBACK_LENGTH = 140;
const static int MIN_LOOKBACK_LENGTH = 60;
const static int MIN_EMA_LENGTH = 1; 
const static int MAX_EMA_LENGTH = 50; 
const static double STARTING_CAPITAL = 450.0; 
const static double TX_FEE_RATE = 0.0;


void find_optimal_dynema(const float price_data[], const int start_day_idx, double* result_table[], const int price_data_size) { 
    #pragma omp parallel for
    for (int i = MIN_READJUSTMENT_TIME; i <= MAX_READJUSTMENT_TIME; i++) { 
        for (int j = MIN_LOOKBACK_LENGTH; j <= MAX_LOOKBACK_LENGTH; j++) {
            result_table[i - MIN_READJUSTMENT_TIME][j - MIN_LOOKBACK_LENGTH] = simulate_dynamic_ema(price_data, start_day_idx, i, j, price_data_size);
        }
    }
} 


double simulate_dynamic_ema(const float price_data[], const int start_day_idx, const int readjustment_time, const int lookback_length, const int price_data_size) { 
//    cout << "lookback_length: " << lookback_length << endl; 
    ResultStruct optimal_ema = find_optimal_ema(price_data, start_day_idx - lookback_length, start_day_idx -1, price_data_size); 
    int ema_length = optimal_ema.ema_length;
    double price_movement_threshold = optimal_ema.price_movement_threshold; 
    
    double sum_for_avg = 0;  
    int els_added = 0; 
    int k; 
    for (k = start_day_idx - 1 - ema_length; k < start_day_idx - 1; ++k, ++els_added)
    {  
        sum_for_avg += price_data[k];
    }
//    cout << k << " " << start_day_idx - 1 << endl;
    
//    cout << "in simulate_dynamic_ema() -- (optimal) ema_length: " << ema_length << endl;
//    cout << "in simulate_dynamic_ema() -- els_added: " << els_added << endl; 
//    exit(0); 

    double sma = sum_for_avg / ema_length; 
    int smoothing_factor = 2; 
    double multiplier = smoothing_factor / (ema_length + 1); 
    double start_day_price = price_data[k]; 
    double ema = start_day_price * multiplier + sma * (1 - multiplier); 
    
    // set up some simulation variables
    double coins_owned = 0;
    double cash_money = STARTING_CAPITAL;
    bool bought = false;

    // record some data for computation of market returns
    double today_price = price_data[start_day_idx]; 
    double max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
    double initial_coin_purchase = max_purchase_amt / today_price;
    int days_since_update = 0; 
    for (int i = start_day_idx; i < price_data_size; i++) 
    {
        today_price = price_data[i]; 
        double signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold));
//        cout << today_price << " " << signal_price << endl;
        if (bought == false && today_price > signal_price) { 
            bought = true;   
            max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
            cash_money = 0;
            coins_owned += max_purchase_amt / today_price; 
//            cout << "bought " << coins_owned << " @ " << today_price << endl;
        } 
        else if (bought == true && today_price < signal_price) { 
            bought = false; 
            cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE); 
//            cout << "sold " << coins_owned << " @ " << today_price << endl;
            coins_owned = 0; 
        }
       
        ++days_since_update;
        if (days_since_update % readjustment_time == 0) {
            //cout << i - lookback_length + 1 << " " << i << endl; 
            optimal_ema = find_optimal_ema(price_data, i - lookback_length + 1, i, price_data_size);
            ema_length = optimal_ema.ema_length;
            price_movement_threshold =  optimal_ema.price_movement_threshold;
            multiplier = smoothing_factor / (ema_length + 1); 
//            cout << "updated ema to " << ema
        } 

        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier);  
    }
 
    if (bought) { 
        cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE) ;
    } 
    
    double algo_returns = (cash_money - STARTING_CAPITAL) / STARTING_CAPITAL;
    double market_returns = (initial_coin_purchase * today_price / (1 + TX_FEE_RATE) - STARTING_CAPITAL) / STARTING_CAPITAL; 

    return algo_returns - market_returns;
}


ResultStruct find_optimal_ema(const float price_data[], const int start_day_idx, const int last_day_idx, const int price_data_size) { 
    ResultStruct best_performer{-1, -1, -100000.0}; 
//    bool print = true; 
    for (int ema_length = 1; ema_length <= MAX_EMA_LENGTH; ema_length++) 
    { 
        for (int price_movement_threshold = 5; price_movement_threshold <= 100; price_movement_threshold++)
        {
//            double this_run = simulate_ema(price_data, start_day_idx, last_day_idx, ema_length, price_movement_threshold / 1000.0, price_data_size, print);  
            double this_run = simulate_ema(price_data, start_day_idx, last_day_idx, ema_length, price_movement_threshold / 1000.0, price_data_size);  
            best_performer = best_performer.performance_metric > this_run ? best_performer : ResultStruct{ema_length, price_movement_threshold / 1000.0, this_run};
//            print = false; 
        } 
    }
    return best_performer;
}


//
// VERIFIED that sizes of data are correct
//
double simulate_ema(const float price_data[], const int start_day_idx, const int last_day_idx, const int ema_length, const double price_movement_threshold, const int price_data_size) { 
    // compute an sma to start
    double sum_for_avg = 0;  
    int els_added = 0; 
    int k;  
    for (k = start_day_idx - 1 - ema_length; k < start_day_idx - 1;  ++k)
    { 
        sum_for_avg += price_data[k];
        ++els_added;
    }

//    cout << "in simulate_ema() -- ema_length: " << ema_length << endl; 
//    cout << "in simulate_ema() -- els_added: " << els_added << endl; 

    // compute the ema
    double sma = sum_for_avg / ema_length; 
    const int smoothing_factor = 2; 
    double multiplier = smoothing_factor / (double)(ema_length + 1); 
    double start_day_price = price_data[k];
    double ema = start_day_price * multiplier + sma * (1 - multiplier); 
            
    // set up some simulation variables
    double coins_owned = 0; 
    double cash_money = STARTING_CAPITAL; 
    bool bought = false; 

    // record some data for computation of market returns
    double today_price = price_data[start_day_idx]; 
    double max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
    double initial_coin_purchase = max_purchase_amt / today_price; 
    int days_simulated = 0;
    for (int i = start_day_idx ; i <= last_day_idx; ++i) 
    {   
        today_price = price_data[i]; 
        double signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 - price_movement_threshold)); 
//        double signal_price;
//        if (!bought)
//            signal_price = ema * (1 + price_movement_threshold);
//        else 
//            signal_price = ema * (1 - price_movement_threshold); 

        if (bought == false && today_price > signal_price) { 
            bought = true;   
            max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
            cash_money = 0; 
            coins_owned += max_purchase_amt / today_price; 
        } 
        else if (bought == true && today_price < signal_price) { 
            bought = false; 
            cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE); 
            coins_owned = 0; 
        }

        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier); 
        ++days_simulated;
    }
    
//    if (print) {
//        for (int i = last_day_idx - 4; i <= last_day_idx; i++) { 
//            cout << price_data[i] << ", " ;
//        }
//        cout << endl;
//    }

//    cout << "in simulate_ema() -- days_simulated: " << days_simulated << endl; 

    if (bought) {
        cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE); 
    }
    
    double algo_returns = (cash_money - STARTING_CAPITAL) / STARTING_CAPITAL; 
    double market_returns = (initial_coin_purchase * today_price / (1 + TX_FEE_RATE) - STARTING_CAPITAL) / STARTING_CAPITAL; 
//    cout << "algo_returns: " << algo_returns << endl;  
//    cout << "market_returns: " << market_returns << endl;  
    return algo_returns - market_returns; 
}


int main(int argc, char* args[]) {
    const static int DATA1_LENGTH = 252;  
    const static int DATA2_LENGTH = 1259;  

    if (argc <= 2) {
        cout << "must enter history and simulation data files" << endl;
        return 1;    
    }

    ifstream historic_data_file(args[1], fstream::in); 
    ifstream sim_data_file(args[2], fstream::in);

    if (!historic_data_file.is_open() || !sim_data_file.is_open()){ 
        cout << "File open error" << endl;
        return 1; 
    }

    // an array to hold all of the price data
    float price_data[DATA1_LENGTH + DATA2_LENGTH]; 

    string line;
    int i = 0;
    // discard header
    getline(historic_data_file, line); 
    
    while ( getline(historic_data_file, line) ) { price_data[i++] = stof(line); }

    // discard header
    getline(sim_data_file, line); 
    while ( getline(sim_data_file, line) ) { price_data[i++] = stof(line); }

    // make a table for results
    double ** results = new double*[MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1]; 
    for (int i = 0; i < MAX_READJUSTMENT_TIME - MIN_READJUSTMENT_TIME + 1; i++) { 
        results[i] = new double[MAX_LOOKBACK_LENGTH - MIN_LOOKBACK_LENGTH + 1]; }

    // simulate and report results
    find_optimal_dynema(price_data, DATA1_LENGTH, results, DATA1_LENGTH + DATA2_LENGTH);
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


