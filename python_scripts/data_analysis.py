import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


coords_1_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_1"
coords_2_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_2"
coords_3_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_3"
coordpaths = [coords_1_path, coords_2_path, coords_3_path]

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
times = ['00-00', '01-00', '02-00', '03-00', '04-00', '05-00', '06-00', '07-00', '08-00', '09-00', '10-00', '11-00', '12-00', '13-00', '14-00', '15-00', '16-00', '17-00', '18-00', '19-00', '20-00', '21-00', '22-00', '23-00']

area_dict = {}
for day in days:
    area_dict[day] = {}
    for time in times:
        area_dict[day][time] = [0, 0] # 1st digit total area, 2nd digit number of instances

# creating pandas df with the days as columns and times for the row index
table = pd.DataFrame(columns=days, index=times)

for path in coordpaths:
    for file_name in os.listdir(path):
        parts = file_name.split('_')
        date = parts[0]
        time = parts[1]
        day = parts[2][:3]
        area_dict[day][time][1] += 1
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r') as file:
            total_box_area = 0
            for line in file:
                numbers = line.split()
                x = float(numbers[1])
                actual_y = float(numbers[2])
                y = 1 / (1 + np.exp(4 * (x - 0.73)))
                if actual_y < y:
                    box_area = float(numbers[3]) * float(numbers[4])
                    total_box_area += box_area
            area_dict[day][time][0] += total_box_area
            total_area = area_dict[day][time][0]
            instance_no = area_dict[day][time][1]
            table.loc[time, day] = total_area/instance_no

# applying min-max scaling to the table
max_value = table.max().max()
table = table.astype(float)
table = table/max_value * 5 # scaled values range from 0 to 5; 0 = no jam, 5 = very congested, then rounding to 2dp for readability
table = table.apply(lambda x: x.round(2))
print(table)
# table.to_csv('sorted_data.csv', index=False)

d = 0
color = ['red', 'blue', 'green', 'yellow', 'black', 'purple', 'pink']
fig, axes = plt.subplots(2, 4)
axesrows = [0, 0, 0, 0, 1, 1, 1]
axescols = [0, 1, 2, 3, 0, 1, 2]
for col in table.columns:
    y = list(table[col])
    # plt.plot(times, y, label=days[d], color=color[d])
    axes[axesrows[d], axescols[d]].bar(range(24), y)
    axes[axesrows[d], axescols[d]].set_xticks(range(24))
    axes[axesrows[d], axescols[d]].set_xticklabels(times, rotation=66, fontsize=7)
    axes[axesrows[d], axescols[d]].set_title(days[d])
    axes[axesrows[d], axescols[d]].set_ylim(0, 5)
    d += 1
axes[1, 3].axis('off')
plt.show()

# plt.title('Area of each day at different times')
# plt.xlabel('time')
# plt.ylabel('area')
# plt.legend()
# plt.grid(True)
# plt.show()