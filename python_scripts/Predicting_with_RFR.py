import pandas as pd
from sklearn.model_selection import train_test_split, KFold
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

# Random Forest Regressor model
def train_test_rfr(X, y, column_name=None, save_model=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    rfr_model = RandomForestRegressor()
    rfr_model.fit(X_train, y_train)
    rfr_predictions = rfr_model.predict(X_test)
    # X_test['congestion_prediction'] = list(rfr_predictions)
    rfr_mae = mean_absolute_error(y_test, rfr_predictions)
    rfr_rmse = mean_squared_error(y_test, rfr_predictions)**0.5
    mae_to_rmse = rfr_rmse/rfr_mae
    print(f"rfr mae: {rfr_mae} ")
    print(f"rfr rmse: {rfr_rmse} ")
    print(f'ratio: {mae_to_rmse}')
    if column_name:
        new_row = [column_name, rfr_mae, rfr_rmse, mae_to_rmse]
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




