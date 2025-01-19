import os

coordsfolder_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_1"

coords_filenames = os.listdir(coordsfolder_path)

number = 1
for name in coords_filenames:
    from_path = f"GCloud\\snaps since dec 27th\\{name[:-3]}jpg"
    to_path = f"GCloud\\snaps_1\\{name[:-3]}jpg"
    os.rename(from_path, to_path)
    print(number)
    number += 1
    
