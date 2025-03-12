import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv(r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\miscellaneous\newdata.csv")
dontneedtime = df.pop('Time of Day')
y_column_jb = df.pop('congestion_scale_jb')
y_column_wdlands = df.pop('congestion_scale_wdlands')
X_train, X_test, y_train, y_test = train_test_split(df, y_column_jb, test_size=0.2, random_state=0) # start of with jb

# Random Forest Regressor model
rfr_model = RandomForestRegressor()
rfr_model.fit(X_train, y_train)
rfr_predictions = rfr_model.predict(X_test)
X_test['congestion_prediction'] = list(rfr_predictions)
rfr_mae = mean_absolute_error(y_test, rfr_predictions)
rfr_rmse = mean_squared_error(y_test, rfr_predictions)**0.5
mae_to_rmse = rfr_rmse/rfr_mae
print(f"rfr mae: {rfr_mae} ")
print(f"rfr rmse: {rfr_rmse} ")
print(f'ratio: {mae_to_rmse}')
# joblib.dump(rfr_model, "rfr_model_jb.joblib") # saving rfr weights for App Engine

# # Decision Tree Model
# dtr_model = DecisionTreeRegressor()
# dtr_model.fit(X_train, y_train)
# dtr_predictions = dtr_model.predict(X_test)
# print(f'dtr mae: {mean_absolute_error(y_test, dtr_predictions)} ')
# print(f"dtr mse: {mean_squared_error(y_test, dtr_predictions)} ")
# print(X_test.head(20))
