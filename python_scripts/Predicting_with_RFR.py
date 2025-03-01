import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv('newdata.csv')
y_column_jb = df.pop('congestion_scale_jb')
y_column_wdlands = df.pop('congestion_scale_wdlands')
X_train, X_test, y_train, y_test = train_test_split(df, y_column_jb, test_size=0.2, random_state=0) # start of with jb

# Random Forest Regressor model
rfr_model = RandomForestRegressor()
rfr_model.fit(X_train, y_train)
# joblib.dump(rfr_model, "rfr_model.joblib") # saving rfr weights for App Engine

rfr_predictions = rfr_model.predict(X_test)
X_test['congestion_prediction'] = list(rfr_predictions)
print(X_test.head(20))
print(mean_absolute_error(y_test, rfr_predictions))
print(mean_squared_error(y_test, rfr_predictions))