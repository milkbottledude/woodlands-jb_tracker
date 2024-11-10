import os
import pandas as pd
import numpy as np

# first, imma make a blank slate df with days for columns and timestamps for indexes
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
times = ['00-00', '01-00', '02-00', '03-00', '04-00', '05-00', '06-00', '07-00', '08-00', '09-00', '10-00', '11-00', '12-00', '13-00', '14-00', '15-00', '16-00', '17-00', '18-00', '19-00', '20-00', '21-00', '22-00', '23-00']
df = pd.DataFrame(np.nan, index=times, columns=days)

# creating a dictionary to temporary store all the values:
data = {}
# now ill iterate thru the folder for the txt files which contain the bounding box details of each image
folder_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\datetimes"
greatest_area = 0.114414865221
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    day, date, time = filename.split('_')
    time = time[:-4]
    total_area = 0
    with open(file_path, 'r') as file:
        for line in file:
            nums = line.split()
            # the 2nd last value in each line is the width of the bounding box, and the last value the height
            width = nums[-2]
            height = nums[-1]
            area = float(width) * float(height)
            total_area += area
    # simplifying the area by performing a simple min-max scaling on the value, makes the values easier to understand, then rounding to 3dp
    total_area = total_area/greatest_area
    if f'{day}_{time}' in data:
        data[f'{day}_{time}'].append(total_area)
    else:
        data[f'{day}_{time}'] = [total_area]
# now we can find the average of the values by dividing the sum of the numbers in each list by the length of the list
for key, value in data.items():
    avg = str(sum(value)/len(value))[:5]
    day, time = key.split('_')
    # adding the average value to the pandas df
    df.at[time, day] = float(avg)
print(df)

# exporting df to csv file
df.to_csv('sorteddata.csv', index=True)