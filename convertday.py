import os

# Path to the folder where your JPEG files are located
folder_path = r"C:\\Users\\Yu Zen\\Documents\\Coding\\Project-JBridge\\GCloud\\coords_1"

for filename in os.listdir(folder_path):
    parts = filename.split('_')
    day = parts[0][:3]
    time = parts[2][:5]
    print(time)
    new_filename = f"{parts[1]}_{time}_{day}.txt"
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)
    os.rename(old_file, new_file)
    print(f"Renamed: {filename} -> {new_filename}")

