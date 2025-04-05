import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib




df = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\newdata.csv")
df_to_attach = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\data_to_attach.csv")

# final_data_df = pd.concat([df, df_to_attach], axis=1)
# final_data_df.to_csv('final_data.csv', index=False)

dontneedtime = df.pop('Time of Day')
dontneedfulldate = df_to_attach.pop('full_date_ymd')
remove_holperiods_first = df_to_attach.drop(['sch_hol_period', 'public_hol_period'], axis=1)

df_loss = pd.DataFrame(columns=['feature', 'mae', 'rmse', 'mae_to_rmse ratio'])

rfr_model = RandomForestRegressor()
# Random Forest Regressor model
def train_test_rfr(X, y, model=rfr_model, column_name=None, save_model=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model.fit(X_train, y_train)
    rfr_predictions = model.predict(X_test)
    # X_test['congestion_prediction'] = list(rfr_predictions)
    rfr_mae = mean_absolute_error(y_test, rfr_predictions)
    rfr_rmse = mean_squared_error(y_test, rfr_predictions)**0.5
    rmse_to_mae = rfr_rmse/rfr_mae
    print(f"rfr mae: {rfr_mae} ")
    print(f"rfr rmse: {rfr_rmse} ")
    print(f'ratio: {rmse_to_mae}')
    if column_name:
        new_row = [column_name, rfr_mae, rfr_rmse, rmse_to_mae]
        df_loss.loc[len(df_loss)] = new_row
    if save_model == True:
        joblib.dump(rfr_model, "rfr_model_jb.joblib") # saving rfr weights for App Engine


# going thru new features
new_features = []
# for feature_name in df_to_attach:
#     new_features.append(feature_name)

y_column_jb = df.pop('congestion_scale_jb')
y_column_wdlands = df.pop('congestion_scale_wdlands')

def testing_new_features(to_csv=False):
    for feature_name in new_features:
        df[feature_name] = df_to_attach[feature_name]
        print(feature_name)
        train_test_rfr(df, y_column_wdlands, feature_name) # choose y value depending on which road you want to test (REM)
        print(f'{feature_name} done')
        df.drop(feature_name, axis=1)
    print(df_loss)
    if to_csv:
        df_loss.to_csv('loss_data_wdlands.csv', index=False)

final_df = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\final_data.csv")
final_df = final_df.drop(['exact_date_value', 'Time of Day', 'full_date_ymd', 'congestion_scale_jb', 'congestion_scale_wdlands'], axis=1)

# using k folds val to test generalization
def cross_val(model=rfr_model, X=final_df, y=y_column_jb):
    losses = cross_val_score(model, X, y, cv=8, scoring='neg_mean_absolute_error')
    losses = np.abs(losses)
    for x in range(len(losses)):
        print(f'fold {x}: {losses[x]}')
    print(f'average mae: {np.mean(losses)}')

# one-hot encoding of month here, adding the column from final_data.csv
def one_hot_month():
    month = final_df.pop('month')
    df['month'] = month
    df = pd.get_dummies(df, columns=['month'])
    print(df.head(5))

# one-hot encoding for quarters of a year, using month column
def one_hot_quarter(df=df):
    def quarter_col(month_value):
        if month_value <= 3:
            return 'Q1'
        elif month_value <= 6:
            return 'Q2'
        elif month_value <= 9:
            return 'Q3'
        else:
            return 'Q4'
        
    df['month'] = final_df['month']
    df['year_quarter'] = df['month'].apply(quarter_col)
    df = df.drop(['month'], axis=1)
    df = pd.get_dummies(df, columns=['year_quarter'])
    print(df.columns)
    df = df.drop(['year_quarter_Q4'], axis=1)
    train_test_rfr(df, y_column_jb)

one_hot_quarter()