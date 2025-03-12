import os
import pandas as pd
import numpy as np

s4_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_4"
s4_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps4_250225_103255.txt"

s5_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_5"
s5_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps5_250225_163710.txt"

s6_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_6"
s6_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps6_250225_174508.txt"

s7_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_7"
s7_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps7_250226_110515.txt"

pic_paths_list = [s4_pics, s5_pics, s6_pics, s7_pics]
scale_paths_list = [s4_scale, s5_scale, s6_scale, s7_scale]

column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Time of Day', 'hour_sin', 'hour_cos', 'congestion_scale_jb', 'congestion_scale_wdlands']
df = pd.DataFrame(columns=column_names)

for scale_path in scale_paths_list:
    pics_index = 0
    with open(scale_paths_list[0], "r") as file:
        pic_index = 0
        for line in file:
            scale_jb = int(line[0])
            scale_wdlands = int(line[1])
            file_name = os.listdir(pic_paths_list[pics_index])[pic_index]
            parts = file_name.split('_')
            date = parts[0]
            time = int(parts[1][:2])
            day = parts[2][:3]
            index = None
            for i in range(6):
                if day == column_names[i]:
                    index = i
                    break
            hour_sin = np.sin(2 * np.pi * time / 24)
            hour_cos = np.cos(2 * np.pi * time / 24)
            new_row = [0, 0, 0, 0, 0, 0, time, hour_sin, hour_cos, scale_jb, scale_wdlands]
            # print(new_row)
            if index:
                new_row[index] = 1
            df.loc[len(df)] = new_row
            pic_index += 1
    pics_index += 1

# print(df.head(40))

df.to_csv('newdata.csv', index=False)