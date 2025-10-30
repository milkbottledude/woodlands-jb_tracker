from datetime import datetime
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import lightgbm as lgb


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



def rating_to_df(rating_path, own_rating=False):
    cols = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos', 'sch_hol_period', 'public_hol_period', 'year_quarter_Q1', 'year_quarter_Q2', 'year_quarter_Q3']
    addition_df = pd.DataFrame(columns=cols)
    with open(rating_path, 'r') as f:
        content = f.readlines()
        line_no = 1
        for line in content:
            input_dfrow = pd.DataFrame(np.zeros((1, len(cols))), columns=cols)
            separation = line.split(' ')
            # getting ratings, the 'y value'
            # ratings = separation[1]
            jb_rating = None # ratings[0]
            wdlands_rating = None # ratings[1]
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
            if not own_rating:
                input_dfrow['congestion_scale_jb'] = jb_rating
                input_dfrow['congestion_scale_wdlands'] = wdlands_rating
            # connecting row to addition_df
            addition_df = pd.concat([addition_df, input_dfrow], axis=0, ignore_index=True)
            print(line_no)
            # print(addition_df.columns)
            line_no += 1
    return addition_df
        
# test run 'rating_to_df' function (SUCCESS: 8, 9, 10)
rating_no = 11
def test1(x, own_r):
    return rating_to_df(fr"C:\Coding\Project-JBridge\GCloud\rating_{x}.txt", own_rating=own_r)


# 'df_to_csv' function
def df_to_csv(addition_df, csv_path, csv_empty=False):
    if csv_empty:
        addition_df.to_csv(csv_path, mode='a', header=True, index=False)
    else:
        addition_df.to_csv(csv_path, mode='a', header=False, index=False)
    print("to csv'ed")
    return addition_df

# test run 'df_to_csv' function, need to test with test1 to work (SUCCESS: 8, 9, 10)
def test2(test1_result, csv_path):
    return df_to_csv(test1_result, csv_path)

# for i in range(8, 33): # 20-32, excluding 33
#     test2(test1(i), r'python_scripts\REAL_finaldataFULL.csv')

test_results_csv_path = 'modeltest_results.csv'
# 'csv_to_joblib' function
def csv_to_modeltest_or_joblib(rating_range, jb_or_wdlands, data_csv_path, version, results_csv_path = 'modeltest_results.csv', joblibb=False, xgboosttt=False, model_='rfr'):
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
            y = y_column_jb
            hyperparams = rfr_model_jb_hyperparams
            if model_ == 'lgb':
                model = lgb.LGBMRegressor(
                    device = 'gpu',
                    num_leaves = 35,
                    n_estimators = 131
                )
            elif xgboosttt:
                model = xgb.XGBRegressor(**hyperparams)
            else:
                model = RandomForestRegressor(**hyperparams)
            print('jb selected for testing')
        else:
            y = y_column_wdlands
            hyperparams = rfr_model_wdlands_hyperparams
            if model_ == 'lgb':
                model = lgb.LGBMRegressor(
                    device = 'gpu',
                    num_leaves = 35,
                    n_estimators = 131
                )
            elif xgboosttt:
                model = xgb.XGBRegressor(**hyperparams)
            else:
                model = RandomForestRegressor(**hyperparams)
            print('wdlands selected for testing')

        X_train, X_test, y_train, y_test = train_test_split(trainfinal_df, y, test_size=0.3, random_state=0)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions)**0.5
        print(f"{model_} mae: {round(mae, 5)} ")
        print(f"{model_} rmse: {round(rmse, 5)} ")
        date_time = datetime.now()
        date_time = date_time.strftime('%Y-%m-%d %H:%M')
        test_results_df = pd.DataFrame(columns=['datetime', 'road_to', 'ratings_used', 'custom_hyperparameters', 'mae', 'rmse', 'model'])
        test_results_df.loc[0] = [date_time, jb_or_wdlands, rating_range, hyperparams, mae, rmse, model_]
        test_results_df.to_csv(results_csv_path, mode='a', header=False, index=False) # disable header=True


    else:
        if jb_or_wdlands == 'jb':
            # hyperparams = rfr_model_jb_hyperparams
            # model = RandomForestRegressor(**hyperparams)
            model = lgb.LGBMRegressor(
                device = 'gpu',
                num_leaves = 35,
                n_estimators = 131
            )
            model.fit(trainfinal_df, y_column_jb)
            # joblib.dump(model, f'rfr_model_jb_v{str(version)}.joblib')
            model.booster_.save_model(f"lgbm_model_jb_v{str(version)}.txt") 
            # print('jb joblibbed')

        else:
            # hyperparams = rfr_model_wdlands_hyperparams
            model = lgb.LGBMRegressor(
                device = 'gpu',
                num_leaves = 35,
                n_estimators = 131
            )
            # model = RandomForestRegressor(**hyperparams)
            model.fit(trainfinal_df, y_column_wdlands)
            # joblib.dump(model, f'rfr_model_wdlands_v{str(version)}.joblib')
            model.booster_.save_model(f"lgbm_model_wdlands_v{str(version)}.txt") 
            # print('wdlands joblibbed')


# test run 'csv_to_modeltest_or_joblib' function (SUCCESS: 8, 9, 10)
def test3(ratings_range, jb_or_wdlands, data_csv_path, version, model_='lgb'):
    csv_to_modeltest_or_joblib(ratings_range, jb_or_wdlands, data_csv_path, version, model_=model_)

# test3('8-32', 'jb', 'python_scripts/RN_finaldayta_8_40.csv', 3, 'lgb')


# in data_v4.csv, ratings 4-7 is till line 752, lines 753-3163 is ratings 8-19


# WAIT HOLUP THE TEST IS AGAINST ITS OWN % OF TEST DATA, SO NO WONDER THE ERROR IS GETTING WORSE AND WORSE, SHOULD TEST AGAINST A FRACTION OF THE ENTIRE SHIT, use 'trainfinal_data.csv' for the testing, but still use only 80% for train data when testing K BYEEE
# v4 = rating 8-19
# v5 = ratings 4-19 

# ['03-02', '22-00', 'Sun']



# LGBM_v1 VS RFR_v5

lgbm_jb_v2 = lgb.Booster(model_file="lgbm_model_jb_v2.txt")
rfr_model_v5 = joblib.load("rfr_model_jb_v5.joblib")
csv_path = "finaldata_20_to_32.csv"

def lgbm_vs_rfr(data_csv_path, models=list):
    data_df = pd.read_csv(data_csv_path)
    print(data_df.columns)
    val_y = data_df.pop('congestion_scale_jb')
    y_column_wdlands = data_df.pop('congestion_scale_wdlands')
    num = 1
    for model in models:
        pred = model.predict(data_df)
        rmse = np.sqrt(mean_squared_error(pred, val_y))
        mae = mean_absolute_error(pred, val_y)

        print(f'model_{num}_rmse: {round(rmse, 3)}')
        print(f'model_{num}_me: {round(mae, 3)}')
        num += 1

# lgbm_vs_rfr(csv_path, [lgbm_jb_v1, rfr_model_v5])




# #TESTING TRAIN TEST SPLIT REPLICABILITY W DIFF DFs

ril_df = pd.read_csv('python_scripts/REAL_finaldataFULL.csv')
ril_y_jb = ril_df.pop('congestion_scale_jb')
ril_y_wdlands = ril_df.pop('congestion_scale_wdlands')
fek_df = pd.read_csv('rating_w_resnet/RN_finaldaytaFULL.csv')
fek_y = fek_df.pop('jb_rating')

ril_X_train, ril_X_test, ril_y_train, ril_y_test = train_test_split(ril_df, ril_y_jb, test_size=0.3, random_state=0)
fek_X_train, fek_X_test, fek_y_train, fek_y_test = train_test_split(fek_df, fek_y, test_size=0.3, random_state=0)

# print('X_train comparison')
# print(ril_X_train.head(5))
# print(fek_X_train.head(5))

# print('X_test comparison')
# print(ril_X_test.head(5))
# print(fek_X_test.head(5))


# Testing model trained on ril data, vs fek data (rated by RN rater)

def ril_or_fek(y_train, ril=bool, train=True, model_path=False):
    if train:
        model = lgb.LGBMRegressor(
            device = 'gpu',
            num_leaves = 35,
            n_estimators = 131
        )
        model.fit(ril_X_train, y_train)
    else:
        # model = lgb.Booster(model_file=model_path)
        model = joblib.load('rfr_model_jb_v5.joblib')
    predictions = model.predict(ril_X_test)
    mae = mean_absolute_error(ril_y_test, predictions)
    rmse = mean_squared_error(ril_y_test, predictions)**0.5
    which = 'fek'
    if ril:
        which = 'ril'
    print(f"{which} mae: {round(mae, 5)} ")
    print(f"{which} rmse: {round(rmse, 5)} ")

# ril_or_fek(fek_y_train, ril=False)

# LightGBM incremental training

incremental_csv_path = r'rating_w_resnet\RNdayta_33_40.csv'
lightgbm_jb_model_path = 'lgbm_model_jb_v2.txt'
# lightgbm_wdlnd_model_path = 'CMGSOON.txt'

def incr_gbm_trng(incr_csv_path, lgb_model_path, to_where='jb'):
    incr_df = pd.read_csv(incr_csv_path)
    if to_where == 'jb':
        y_rn = incr_df.pop('jb_rating')
    elif to_where =='wdlands':
        y_rn = incr_df.pop('wdlands rating')

    for i in range(33, 41):
        test2(test1(i, own_r=True), r'rating_w_resnet\w_cols_33_40.csv')

    full_df = pd.read_csv(r'rating_w_resnet\w_cols_33_40.csv')
    print(full_df)
    lgb_dataset = lgb.Dataset(full_df, label=y_rn)

    params = {
        'device': 'gpu',
        'num_leaves': 35,
        'n_estimators': 131
    }

    incr_model = lgb.train(
        params,
        lgb_dataset,
        # num_boost_round=50, # adds more trees cos more data ukwim
        init_model=lgb_model_path  # Pass path directly
    )

    incr_model.save_model(f'{to_where}_incrLGBM_model_v1.txt')

incr_gbm_trng(incremental_csv_path, lightgbm_jb_model_path)