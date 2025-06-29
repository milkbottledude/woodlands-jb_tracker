from datetime import datetime
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


# currently making rfr_model_v4

def week_numbering(exact_date):
    week_no = 1
    for m in range(1, 4):
        if exact_date < m * 7:
            break
        else:
            week_no += 1
    return week_no

year = '-2025'
def mathing_dayofyear(date_obj):
    day_of_year = date_obj.dayofyear
    day_of_year_sined = np.sin(2 * np.pi * day_of_year / 365) # is this the biggest blunder of mankind, putting 'exact_date' instead of 'day_of_year'
    day_of_year_cosed = np.cos(2 * np.pi * day_of_year / 365)
    return [day_of_year, day_of_year_sined, day_of_year_cosed]

def holidating(date_obj):
    sch_hols_periods = [['2024-11-23', '2024-12-31'], ['2025-3-15', '2025-3-23'], ['2025-5-31', '2025-6-29'], ['2025-9-6', '2025-9-14'], ['2025-11-22', '2026-1-1']]
    public_hols_periods = [['2025-1-28', '2025-1-31'], ['2025-3-29', '2025-3-31'], ['2025-6-5', '2025-6-12'], ['2025-10-17', '2025-10-20'], ['2025-12-23', '2025-12-26']]
    sch_hol_period = False
    for sch_period in sch_hols_periods:
        start = pd.to_datetime(sch_period[0])
        end = pd.to_datetime(sch_period[1])
        if date_obj > start:
            if date_obj < end:
                sch_hol_period = True
                break

    public_hol_period = False
    for public_period in public_hols_periods:
        start = pd.to_datetime(public_period[0])
        end = pd.to_datetime(public_period[1])
        if date_obj > start:
            if date_obj < end:
                public_hol_period = True
                break
    
    return [sch_hol_period, public_hol_period]



def rating_to_df(rating_path):
    cols = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos', 'sch_hol_period', 'public_hol_period', 'year_quarter_Q1', 'year_quarter_Q2', 'year_quarter_Q3']
    addition_df = pd.DataFrame(columns=cols)
    with open(rating_path, 'r') as f:
        content = f.readlines()
        line_no = 1
        for line in content:
            input_dfrow = pd.DataFrame(np.zeros((1, len(cols))), columns=cols)
            separation = line.split(' ')
            # getting ratings, the 'y value'
            ratings = separation[1]
            jb_rating = ratings[0]
            wdlands_rating = ratings[1]
            info = separation[0][:-4]
            info_parts = info.split('_')
            # getting day of week index (within function)
            day_of_week = info_parts[2]
            if day_of_week != 'Sun':
                input_dfrow[day_of_week] = 1
            # columns 'hour_sin' and 'hour_cos' (within function)
            time24 = float(info_parts[1][:2])
            input_dfrow['hour_sin'] = np.sin(2 * np.pi * time24 / 24)
            input_dfrow['hour_cos'] = np.cos(2 * np.pi * time24 / 24)
            # column 'week_value' (outsourced)
            date = info_parts[0]
            date_parts = date.split('-')
            exact_date = int(date_parts[0])
            week_no = week_numbering(exact_date)
            input_dfrow['week_value'] = week_no
            # columns 'date_sin' and 'date_cos' (within function)
            date_sined = np.sin(2 * np.pi * exact_date / 31)
            date_cosed = np.cos(2 * np.pi * exact_date / 31)
            input_dfrow['date_sin'] = date_sined
            input_dfrow['date_cos'] = date_cosed
            # columns 'day_of_year', 'day_of_year_sin', 'day_of_year_cos' (outsourced)
            date_str = date + year
            date_obj = pd.to_datetime(date_str, format="%m-%d-%Y")
            doy_and_sined_cosed = mathing_dayofyear(date_obj)
            input_dfrow['day_of_year'] = doy_and_sined_cosed[0]
            input_dfrow['day_of_year_sin'] = doy_and_sined_cosed[1]
            input_dfrow['day_of_year_cos'] = doy_and_sined_cosed[2]
            # columns 'sch_hol_period', 'public_hol_period' (outsourced)
            hols_periods = holidating(date_obj)
            input_dfrow['sch_hol_period'] = hols_periods[0]
            input_dfrow['public_hol_period'] = hols_periods[1]
            # columns 'year_quarter_Q1', 'year_quarter_Q2', 'year_quarter_Q3' (within function)
            input_dfrow['year_quarter_Q1'] = False
            input_dfrow['year_quarter_Q2'] = False
            input_dfrow['year_quarter_Q3'] = False
            month_value = int(date_parts[1])
            if month_value <= 3:
                input_dfrow['year_quarter_Q1'] = True
            elif month_value <= 6:
                input_dfrow['year_quarter_Q2'] = True
            elif month_value <= 9:
                input_dfrow['year_quarter_Q3'] = True
            # adding jb and wdlands ratings as the last 2 cols
            input_dfrow['congestion_scale_jb'] = jb_rating
            input_dfrow['congestion_scale_wdlands'] = wdlands_rating
            # connecting row to addition_df
            addition_df = pd.concat([addition_df, input_dfrow], axis=0, ignore_index=True)
            print(line_no)
            print(addition_df.columns)
            line_no += 1
    return addition_df
        
# test run 'rating_to_df' function (SUCCESS: 8, 9, 10)
rating_no = 11
def test1(x):
    return rating_to_df(fr"C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\rating_{x}.txt")


# 'df_to_csv' function
csv_path = r'C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\python_scripts\REAL_finaldataFULL.csv'
def df_to_csv(addition_df, csv_path, csv_empty=False):
    if csv_empty:
        addition_df.to_csv(csv_path, mode='a', header=True, index=False)
    else:
        addition_df.to_csv(csv_path, mode='a', header=False, index=False)
    print("to csv'ed")

# test run 'df_to_csv' function, need to test with test1 to work (SUCCESS: 8, 9, 10)
def test2(test1_result):
    df_to_csv(test1_result, csv_path)


test_results_csv_path = 'modeltest_results.csv'
# 'csv_to_joblib' function
def csv_to_modeltest_or_joblib(rating_range, jb_or_wdlands, data_csv_path=csv_path, results_csv_path = 'modeltest_results.csv', joblibb=False):
    # splitting up csv into x & y variables
    trainfinal_df = pd.read_csv(data_csv_path)
    print(trainfinal_df.columns)
    y_column_jb = trainfinal_df.pop('congestion_scale_jb')
    y_column_wdlands = trainfinal_df.pop('congestion_scale_wdlands')
    
    # random_state=0, max_depth=14, n_estimators=30, max_features=12
    rfr_model_jb_hyperparams = {
        'random_state': 0
    } 

    # random_state=0, max_depth=16, n_estimators=15, max_features=10
    rfr_model_wdlands_hyperparams = {
        'random_state': 0
    }

    if joblibb == False:
        if jb_or_wdlands == 'jb':
            hyperparams = rfr_model_jb_hyperparams
            model = RandomForestRegressor(**hyperparams)
            y = y_column_jb
            print('jb selected for testing')
        else:
            hyperparams = rfr_model_wdlands_hyperparams
            model = RandomForestRegressor(**hyperparams)
            y = y_column_wdlands
            print('wdlands selected for testing')

        X_train, X_test, y_train, y_test = train_test_split(trainfinal_df, y, test_size=0.2, random_state=0)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions)**0.5
        print(f"rfr mae: {mae} ")
        print(f"rfr rmse: {rmse} ")
        date_time = datetime.now()
        date_time = date_time.strftime('%Y-%m-%d %H:%M')
        test_results_df = pd.DataFrame(columns=['datetime', 'road_to', 'ratings_used', 'custom_hyperparameters', 'mae', 'rmse'])
        test_results_df.loc[0] = [date_time, jb_or_wdlands, rating_range, hyperparams, mae, rmse]
        test_results_df.to_csv(results_csv_path, mode='a', header=False, index=False) # disable header=True


    else:
        if jb_or_wdlands == 'jb':
            hyperparams = rfr_model_jb_hyperparams
            model = RandomForestRegressor(**hyperparams)
            model.fit(trainfinal_df, y_column_jb)
            joblib.dump(model, 'rfr_model_jb_v4.joblib')
            print('jb joblibbed')
        else:
            hyperparams = rfr_model_wdlands_hyperparams
            model = RandomForestRegressor(**hyperparams)
            model.fit(trainfinal_df, y_column_wdlands)
            joblib.dump(model, 'rfr_model_wdlands_v4.joblib')
            print('wdlands joblibbed')


# test run 'csv_to_modeltest_or_joblib' function (SUCCESS: 8, 9, 10)
def test3(ratings_range, jb_or_wdlands):
    csv_to_modeltest_or_joblib(ratings_range, jb_or_wdlands)

test3('8-19', 'wdlands')

# 4TH JULY 2025 TASK:  MAKE 'final_data_tillratings7.csv's columns headers the same as that of 'REAL_finaldataFULL.csv'S.


final_part1_csv = pd.read_csv('final_data_tillratings7.csv')
# final_part1_csv['year_quarter_Q1'] = final_part1_csv['mponth']
# final_part1_csv['year_quarter_Q2'] = final_part1_csv
# final_part1_csv['year_quarter_Q3'] = final_part1_csv

final_part2_csv = pd.read_csv('python_scripts\REAL_finaldataFULL.csv')
# final_part1_csv.pop('full_date_ymd')
print(final_part1_csv.columns)
print(final_part2_csv.columns)
# data_v4 = pd.concat([final_part1_csv, final_part2_csv], ignore_index=True)
# print(data_v4)
# print(len(data_v4))
# data_v4.to_csv('data_v4.csv', index=False, header=True)



# WAIT HOLUP THE TEST IS AGAINST ITS OWN % OF TEST DATA, SO NO WONDER THE ERROR IS GETTING WORSE AND WORSE, SHOULD TEST AGAINST A FRACTION OF THE ENTIRE SHIT, use 'trainfinal_data.csv' for the testing, but still use only 80% for train data when testing K BYEEE
# v4 = rating 8-19
# v5 = ratings 4-19 

# ['03-02', '22-00', 'Sun']


# for x in range(15, 20):
#     rating_path_template = fr"C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\rating_{x}.txt"
#   csv_path = 'REAL_finaldataFULL.csv'
#     rating_to_csv(rating_path_template)
#     break