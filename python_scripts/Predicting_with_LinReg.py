import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Time of Day', 'congestion_area']

coords_path_template = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_"

df = pd.DataFrame(columns=column_names)

for num in range(1, 4):
    path = coords_path_template + str(num)
    for file_name in os.listdir(path):
        parts = file_name.split('_')
        date = parts[0]
        time = parts[1]
        day = parts[2][:3]
        index = None
        for i in range(len(column_names)):
            if day == column_names[i]:
                index = i
                break
        total_box_area = 0
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                numbers = line.split()
                x = float(numbers[1])
                actual_y = float(numbers[2])
                y = 1 / (1 + np.exp(4 * (x - 0.73)))
                if actual_y > y:
                    box_area = float(numbers[3]) * float(numbers[4])
                    total_box_area += box_area
        new_row = [0, 0, 0, 0, 0, 0, int(time[:2]), total_box_area]
        if index:
            new_row[index] = 1
        df.loc[len(df)] = new_row

max_value = df['congestion_area'].max().max()
df['congestion_area'] = df['congestion_area']/max_value * 5 # scaled values range from 0 to 5; 0 = no jam, 5 = very congested, then rounding to 2dp for readability
df['congestion_area'] = df['congestion_area'].apply(lambda value: round(value, 2))
print(df)
# 143/517

# getting rid of some rows with 0 congestion_area
df.sort_values(by='congestion_area', ascending=False, inplace=True)
# gonna keep 150 of those rows with congestion_area = 0, so total rows becomes 143 + 150 = 293
df = df.iloc[:293]

# cyclic encoding of time column
df['hour_sin'] = np.sin(2 * np.pi * df['Time of Day'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['Time of Day'] / 24)
df.drop(columns=['Time of Day'], inplace=True)
df.to_csv('train_df_wdlands.csv', index=False)


# # Linear Regression model
# y_column = df.pop('congestion_area')
# model = LinearRegression()
# model.fit(df, y_column)
#
# # making a test df from some unannotated pics
# test_df = pd.DataFrame(columns=column_names[:-1])
# test_snaps_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\test_snaps"
# for file_name in os.listdir(test_snaps_path):
#     parts = file_name.split('_')
#     date = parts[0]
#     time = parts[1]
#     day = parts[2][:3]
#     index = None
#     for i in range(len(column_names)):
#         if day == column_names[i]:
#             index = i
#             break
#     new_test_row = [0, 0, 0, 0, 0, 0, int(time[:2])]
#     if index:
#         new_test_row[index] = 1
#     test_df.loc[len(test_df)] = new_test_row
#
# # cyclic encoding of time column for test_df
# test_df['hour_sin'] = np.sin(2 * np.pi * test_df['Time of Day'] / 24)
# test_df['hour_cos'] = np.cos(2 * np.pi * test_df['Time of Day'] / 24)
# test_df.drop(columns=['Time of Day'], inplace=True)
# test_df.to_csv('test_df.csv', index=False)
#
# predictions = model.predict(test_df)
# test_df['congestion_prediction'] = pd.Series(predictions)
# print(test_df.head(20))
