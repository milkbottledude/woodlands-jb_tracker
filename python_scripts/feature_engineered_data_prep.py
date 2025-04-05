import os
import pandas as pd
import numpy as np
from datetime import datetime
# for correlation matrix;
import seaborn as sns
import matplotlib.pyplot as plt

# getting date details for outdated snaps that dont follow the new rating formatting (snaps 4-8)

pics_folder_template = r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\GCloud\snaps_"

extra_column_names = ['month', 'exact_date_value', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos', 'full_date_ymd']
# df_to_attach = pd.DataFrame(columns=extra_column_names)

def part_one():
    for p in range(4, 8):
        pics_folder_path = pics_folder_template + str(p)
        file_names = os.listdir(pics_folder_path)
        for file_name in file_names:
            parts = file_name.split('_')
            date_parts = parts[0].split('-')
            month = date_parts[0]
            exact_date = int(date_parts[1])
            week_no = 1
            for m in range(1, 4):
                if exact_date < m * 7:
                    break
                else:
                    week_no += 1
            date_sined = np.sin(2 * np.pi * exact_date / 31)
            date_cosed = np.cos(2 * np.pi * exact_date / 31)
            year = '2025-'
            if int(month) >= 9:
                year = '2024-'
            datetime_object = pd.to_datetime(year + str(parts[0]), format='%Y-%m-%d')
            day_of_year = datetime_object.dayofyear
            day_of_year_sined = np.sin(2 * np.pi * exact_date / 365)
            day_of_year_cosed = np.cos(2 * np.pi * exact_date / 365)
            new_row = [month, exact_date, week_no, date_sined, date_cosed, day_of_year, day_of_year_sined, day_of_year_cosed, datetime_object]
            df_to_attach.loc[len(df_to_attach)] = new_row

# part_one()
# df_to_attach.to_csv('data_to_attach.csv', index=False)



# the code below does the same as above, but for ratings 8-14 as they have different formatting

rating_template = r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\GCloud\rating_"

def part_two():
    for x in range(8, 15):
        rating_path = rating_template + str(x) + '.txt'
        with open(rating_path, "r") as file:
            # lines = len(file.readlines()) - 1
            # limit = 0
            for line in file:
                if len(line) < 5:
                    break
                else:
                    parts = line.split('_')
                    date_parts = parts[0].split('-')
                    month = date_parts[0]
                    exact_date = int(date_parts[1])
                    week_no = 1
                    for m in range(1, 4):
                        if exact_date < m * 7:
                            break
                        else:
                            week_no += 1
                    date_sined = np.sin(2 * np.pi * exact_date / 31)
                    date_cosed = np.cos(2 * np.pi * exact_date / 31)
                    year = '2025-'
                    if int(month) >= 9:
                        year = '2024-'
                    datetime_object = pd.to_datetime(year + str(parts[0]), format='%Y-%m-%d')
                    day_of_year = datetime_object.dayofyear
                    day_of_year_sined = np.sin(2 * np.pi * exact_date / 365)
                    day_of_year_cosed = np.cos(2 * np.pi * exact_date / 365)
                    datetime_object = str(datetime_object)[:-9]
                    new_row = [month, exact_date, week_no, date_sined, date_cosed, day_of_year, day_of_year_sined, day_of_year_cosed, datetime_object]
                    df_to_attach.loc[len(df_to_attach)] = new_row
        print(f'{x} done')

# part_two()
# df_to_attach.to_csv('data_to_attach.csv', index=False)



# feature engineering for busy periods (sch hols, public hols, etc) below

sch_hols_periods = [['2024-11-23', '2024-12-31'], ['2025-3-15', '2025-3-23'], ['2025-5-31', '2025-6-29'], ['2025-9-6', '2025-9-14'], ['2025-11-22', '2026-1-1']]

# i added 1-3 days before and after the public hol days, since ppl tend to travel before and after the actual days as well
# Respectively: cny, hari raya puasa, vesak day, hari raya haji, deepavali, christmas
public_hols_periods = [['2025-1-28', '2025-1-31'], ['2025-3-29', '2025-3-31'], ['2025-6-9', '2025-6-12'], ['2025-6-5', '2025-6-8'], ['2025-10-17', '2025-10-20'], ['2025-12-23', '2025-12-26']]

def hol_perioding(df_to_attach):
    df_to_attach['full_date_ymd'] = pd.to_datetime(df_to_attach['full_date_ymd'], format='%Y-%m-%d')
    df_to_attach['sch_hol_period'] = False
    for sch_hol_period in sch_hols_periods:
        df_to_attach['sch_hol_period'] = df_to_attach['sch_hol_period'] | df_to_attach['full_date_ymd'].between(pd.to_datetime(sch_hol_period[0]), pd.to_datetime(sch_hol_period[1]))
    df_to_attach['public_hol_period'] = False
    for public_hol_period in public_hols_periods:    
        df_to_attach['public_hol_period'] = df_to_attach['public_hol_period'] | df_to_attach['full_date_ymd'].between(pd.to_datetime(public_hol_period[0]), pd.to_datetime(public_hol_period[1]))

df_to_attach = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\data_to_attach.csv")
final_df = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\final_data.csv")
month = final_df.pop('month')
final_df.pop('full_date_ymd')
final_df.pop('Time of Day')
final_df.pop('exact_date_value')
# # no hols first
# final_df.pop('sch_hol_period')
# final_df.pop('public_hol_period')

def correlation_heatmap():
    correlation_matrix = final_df.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="RdBu")
    plt.show()

correlation_heatmap()

def count_true(df, column_name):
    count_true = df[column_name].sum()
    print(count_true)
    total_no_of_rows = len(df)
    print(total_no_of_rows)
    print(int(count_true)/total_no_of_rows)

# doing k-fold for hols periods below
