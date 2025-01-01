import os
import pandas as pd
import numpy as np


coords_1_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_1"
coords_2_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_2"
coordpaths = [coords_1_path, coords_2_path]

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
times = ['00-00', '01-00', '02-00', '03-00', '04-00', '05-00', '06-00', '07-00', '08-00', '09-00', '10-00', '11-00', '12-00', '13-00', '14-00', '15-00', '16-00', '17-00', '18-00', '19-00', '20-00', '21-00', '22-00', '23-00']

area_dict = {}
for day in days:
    area_dict[day] = [0, 0] # 1st value is congestion area, 2nd area is for number of images/instances, can use for finding average area over time instances as we might have more of 1 day than another

for path in coordpaths:
    for file_name in os.listdir(path):
        day = file_name[:3]
        area_dict[day][1] += 1
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
            area_dict[day][0] += total_box_area

for key in area_dict:
    area = area_dict[key][0]
    instance_no = area_dict[key][1]
    avg_area = area/instance_no
    area_dict[key].append(avg_area)
    print(key, area_dict[key])