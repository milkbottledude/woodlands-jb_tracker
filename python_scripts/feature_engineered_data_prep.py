import os
import pandas as pd
import numpy as np

# getting date details for outdated snaps that dont follow the new rating formatting (snaps 4-8)

pics_folder_template = r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\GCloud\snaps_"

extra_column_names = ['month', 'exact_date_value', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos']

df_to_attach = pd.DataFrame(columns=extra_column_names)

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
        new_row = [month, exact_date, week_no, date_sined, date_cosed, day_of_year, day_of_year_sined, day_of_year_cosed]
        df_to_attach.loc[len(df_to_attach)] = new_row

df_to_attach.to_csv('data_to_attach.csv', index=False)










# rating_template = r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\GCloud\rating_"

# # df = pd.DataFrame(columns=column_names)
# df = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\newdata.csv")


# for x in range(8, 15):
#     rating_path = rating_template + str(x) + '.txt'
#     with open(rating_path, "r") as file:
#         lines = len(file.readlines()) - 1
#         limit = 0
#         for line in file:
#             if limit == lines:
#                 break
#             else:
#                 scale_jb = int(line[-3])
#                 scale_wdlands = int(line[-2])
#                 file_name = line[:-8]
#                 print(file_name)
#                 parts = file_name.split('_')
#                 date = parts[0]
#                 time = int(parts[1][:2])
#                 day = parts[2][:3]
#                 index = None
#                 for i in range(6):
#                     if day == column_names[i]:
#                         index = i
#                         break
#                 hour_sin = np.sin(2 * np.pi * time / 24)
#                 hour_cos = np.cos(2 * np.pi * time / 24)
#                 new_row = [0, 0, 0, 0, 0, 0, time, hour_sin, hour_cos, scale_jb, scale_wdlands]
#                 # print(new_row)
#                 if index:
#                     new_row[index] = 1
#                 df.loc[len(df)] = new_row
#                 pic_index += 1
#                 limit += 1
#     print(f'{str(x)} done')

# print(df.head(40))

# df.to_csv('newdata_2.csv', index=False)