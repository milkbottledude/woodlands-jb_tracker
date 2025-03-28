import os
import pandas as pd
import numpy as np

# s4_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_4"
# s4_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps4_250225_103255.txt"

# s5_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_5"
# s5_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps5_250225_163710.txt"

# s6_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_6"
# s6_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps6_250225_174508.txt"

# s7_pics = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps_7"
# s7_scale = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps7_250226_110515.txt"

# pic_paths_list = [s4_pics, s5_pics, s6_pics, s7_pics]
# scale_paths_list = [s4_scale, s5_scale, s6_scale, s7_scale]

rating_template = r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\GCloud\rating_"

column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Time of Day', 'hour_sin', 'hour_cos', 'congestion_scale_jb', 'congestion_scale_wdlands']
# df = pd.DataFrame(columns=column_names)
df = pd.read_csv(r"C:\Users\Yu Zen\OneDrive\Coding\Project-JBridge\python_scripts\newdata.csv")


for x in range(8, 15):
    rating_path = rating_template + str(x) + '.txt'
    with open(rating_path, "r") as file:
        lines = len(file.readlines()) - 1
        limit = 0
        for line in file:
            if limit == lines:
                break
            else:
                scale_jb = int(line[-3])
                scale_wdlands = int(line[-2])
                file_name = line[:-8]
                print(file_name)
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
                limit += 1
    print(f'{str(x)} done')

print(df.head(40))

df.to_csv('newdata_2.csv', index=False)