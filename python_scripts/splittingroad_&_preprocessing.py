import os
import matplotlib.pyplot as plt
import numpy as np

folder_path_template = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_"

x_coords = []
y_coords = []
for i in range(1, 4):
    folder_path = folder_path_template + str(i)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                numbers = line.split()
                x_coords.append(float(numbers[1][:4]))
                y_coords.append(float(numbers[2][:4]))

# x = np.linspace(0, 1, 100)
# y = -0.94 * x + 1.18
# plt.plot(x, y, label=str(y))

x_coords_johor = []
y_coords_johor = []
x_coords_wdlands = []
y_coords_wdlands = []
for i in range(len(x_coords)):
    x = x_coords[i]
    actual_y = y_coords[i]
    y = 1 / (1 + np.exp(4 * (x - 0.73)))
    if actual_y < y:
        x_coords_johor.append(x)
        y_coords_johor.append(actual_y)
    else:
        x_coords_wdlands.append(x)
        y_coords_wdlands.append(actual_y)

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid()
x = np.linspace(0, 1, 100)
y = 1 / (1 + np.exp(4 * (x - 0.73)))
plt.plot(x, y, label=str(y))
plt.scatter(x_coords_johor, y_coords_johor, c='blue')
plt.scatter(x_coords_wdlands, y_coords_wdlands, c='red')
plt.xlabel('x')
plt.ylabel('y')
plt.show()