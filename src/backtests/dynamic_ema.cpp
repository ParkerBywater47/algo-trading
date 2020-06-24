#include <iostream>
#include <fstream> 
#include <string>
#include <vector>
#include <cstdlib>
#include <omp.h>

using namespace std;

struct ResultStruct { 
    int ema_length;
    double price_movement_threshold; 
    double performance_metric;
}; 

void find_optimal_dynema(const vector<float> price_data, const int start_day_idx, double* result_table[], const int price_data_size); 
double simulate_dynamic_ema(const vector<float> price_data, const int start_day_idx, const int readjustment_time, const int lookback_length, const int price_data_size); 
ResultStruct find_optimal_ema(const vector<float> price_data, const int start_day_idx, const int last_day_idx, const int price_data_size); 
double simulate_ema(const vector<float> price_data, const int start_day_idx, const int last_day_idx, const int ema_length, const double price_movement_threshold, const int price_data_size);

const static int MAX_READJUSTMENT_TIME = 36; 
const static int MIN_READJUSTMENT_TIME = 7;
const static int MAX_LOOKBACK_LENGTH = 140;
const static int MIN_LOOKBACK_LENGTH = 60;
const static int MIN_EMA_LENGTH = 1;
const static int MAX_EMA_LENGTH = 50; 
const static double STARTING_CAPITAL = 450.0; 
const static double TX_FEE_RATE = 0.0;


double simulate_dynamic_ema(const vector<float> price_data, const int start_day_idx, const int readjustment_time, const int lookback_length, const int price_data_size) { 
    cout << "simulating dynamic ema with readjust time " << readjustment_time << " and lookback length " << lookback_length << endl;
    ResultStruct optimal_ema = find_optimal_ema(price_data, start_day_idx - lookback_length, start_day_idx - 1, price_data_size); 
    int ema_length = optimal_ema.ema_length;
    double price_movement_threshold = optimal_ema.price_movement_threshold; 
    
    double sum_for_avg = 0;  
    int els_added = 0; 
    int k; 
    for (k = start_day_idx - 1 - ema_length; k < start_day_idx - 1; ++k, ++els_added)
    {  
        sum_for_avg += price_data[k];
    }

    double sma = sum_for_avg / ema_length; 
    int smoothing_factor = 2; 
    double multiplier = smoothing_factor / (ema_length + 1); 
    double first_ema_price = price_data[k]; 
    double ema = first_ema_price * multiplier + sma * (1 - multiplier); 
    
    // set up some simulation variables
    double coins_owned = 0;
    double cash_money = STARTING_CAPITAL;
    bool bought = false;

    // record some data for computation of market returns
    double today_price = price_data[start_day_idx]; 
    double max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
    double initial_coin_purchase = max_purchase_amt / today_price;
    double last_buy_price = 0;
    int days_since_update = 0; 
    for (int i = start_day_idx; i < price_data_size; i++) 
    {
        today_price = price_data[i]; 
        double signal_price = ema * (!bought ? (1 + price_movement_threshold) : (1 -price_movement_threshold));
//        cout << today_price << "\t" << signal_price << endl;
        if (bought == false && today_price > signal_price) { 
            bought = true;   
            max_purchase_amt = cash_money / (1 + TX_FEE_RATE); 
            cash_money = 0;
            coins_owned += max_purchase_amt / today_price; 
            last_buy_price = today_price;
//            cout << "bought" << endl;
        } 
        else if (bought == true && today_price < signal_price) { 
            bought = false; 
            cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE); 
//            cout << "sold" << " " << coins_owned * today_price - last_buy_price * coins_owned << endl;
            coins_owned = 0; 
        }
       
        ++days_since_update;
        if (days_since_update % readjustment_time == 0) {
//            cout << "first and last of lookback_days: " << price_data[i - lookback_length] << " " << price_data[i - 1] << endl; 
            optimal_ema = find_optimal_ema(price_data, i - lookback_length + 1, i, price_data_size);
            ema_length = optimal_ema.ema_length;
            price_movement_threshold =  optimal_ema.price_movement_threshold;
            multiplier = smoothing_factor / (ema_length + 1); 
//            cout << "updated ema to " << ema_length << ", " << price_movement_threshold * 100 << "%" << endl;
        } 
        // update exponential moving average  
        ema = today_price * multiplier + ema * (1 - multiplier);  
    }
 
    if (bought) { 
        cash_money += (coins_owned * today_price) / (1 + TX_FEE_RATE) ;
//        cout << "final sell" << " " << coins_owned * today_price - last_buy_price * coins_owned << endl;
    } 
    
    double algo_returns = (cash_money - STARTING_CAPITAL) / STARTING_CAPITAL;
    double market_returns = (initial_coin_purchase * today_price / (1 + TX_FEE_RATE) - STARTING_CAPITAL) / STARTING_CAPITAL; 
   
    printf("%s%.2f%s\n", "algo: ",  algo_returns * 100, "%");
    printf("%s%.2f%s\n", "market: ", market_returns * 100, "%");

    return algo_returns - market_returns;
}


ResultStruct find_optimal_ema(const vector<float> price_data, const int start_day_idx, const int last_day_idx, const int price_data_size) { 
    ResultStruct best_performer{-1, -1, -10000000.0}; 
//    bool print = true; 
    for (int ema_length = MIN_EMA_LENGTH; ema_length <= MAX_EMA_LENGTH; ema_length++) 
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


double simulate_ema(const vector<float> price_data, const int start_day_idx, const int last_day_idx, const int ema_length, const double price_movement_threshold, const int price_data_size) { 
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
//        cout << i << endl;
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
    if (argc <= 3) {
        cout << "must enter historic data file, simulation data file, readjustment time, and lookback length" << endl;
        return 1;    
    }

    const int readjust_time = stoi(args[3]);
    const int lookback_length = stoi(args[4]); 
    int DATA1_LENGTH = 0;
    int DATA2_LENGTH = 0;
    ifstream historic_data_file(args[1], fstream::in); 
    ifstream sim_data_file(args[2], fstream::in);
    
    if (!historic_data_file.is_open() || !sim_data_file.is_open()){ 
        cout << "File open error" << endl;
        exit(1); 
    }

    // an array to hold all of the price data
    vector<float> price_data; 

    string line;
    // discard header
    getline(historic_data_file, line); 
    while ( getline(historic_data_file, line) ) { price_data.push_back(stof(line)); ++DATA1_LENGTH;}

    // discard header
    getline(sim_data_file, line); 
    while ( getline(sim_data_file, line) ) { price_data.push_back(stof(line)); ++DATA2_LENGTH; }
    
    simulate_dynamic_ema(price_data, DATA1_LENGTH, readjust_time, lookback_length, DATA1_LENGTH + DATA2_LENGTH );

    historic_data_file.close();
    sim_data_file.close();
    return 0; 
}


