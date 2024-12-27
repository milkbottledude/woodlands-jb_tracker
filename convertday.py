import os

# Path to the folder where your JPEG files are located
folder_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\datetimes"

# List all files in the directory
for filename in os.listdir(folder_path):
    # Split the filename based on underscores to extract the parts
    parts = filename.split('_')

    # Get the first 3 characters of the day (first part of the filename)
    day_abbr = parts[0][:3]  # Get the first three characters

    # Rebuild the filename using the new day abbreviation
    new_filename = f"{day_abbr}_{'_'.join(parts[1:])}"

    # Create the full path for the old and new filenames
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)

    # Rename the file
    os.rename(old_file, new_file)
    print(f"Renamed: {filename} -> {new_filename}")
