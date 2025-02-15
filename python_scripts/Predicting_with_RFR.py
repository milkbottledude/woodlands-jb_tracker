import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib

train_df = pd.read_csv('train_df.csv')
y_column = train_df.pop('congestion_area')
test_df = pd.read_csv('test_df.csv')

# Random Forest Regressor model
rfr_model = RandomForestRegressor()
rfr_model.fit(train_df, y_column)
joblib.dump(rfr_model, "rfr_model.pkl") # saving rfr weights for App Engine

rfr_predictions = rfr_model.predict(test_df)
test_df['congestion_prediction'] = pd.Series(rfr_predictions)
print(test_df.head(20))

# # Decision Tree Regressor model for shits and giggles
# test_df = pd.read_csv('test_df.csv') # getting test_df again
# dtr_model = DecisionTreeRegressor()
# dtr_model.fit(train_df, y_column)


# dtr_predictions = dtr_model.predict(test_df)
# test_df['congestion_prediction'] = pd.Series(dtr_predictions)
print(test_df.head(20))