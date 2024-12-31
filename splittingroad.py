import os
import matplotlib.pyplot as plt
import numpy as np

# folder_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_1\Sat_11-09_09-00.txt"
folder_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_1"

x_coords = []
y_coords = []
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        for line in file:
            numbers = line.split()
            x_coords.append(float(numbers[1][:4]))
            y_coords.append(float(numbers[2][:4]))

x = np.linspace(0, 1, 100)
y = -0.94 * x + 1.18
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid()
plt.plot(x, y, label=str(y))
plt.plot([0.28, 0.28], [0, 1])
plt.scatter(x_coords, y_coords)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
print(x_coords)
print(y_coords)