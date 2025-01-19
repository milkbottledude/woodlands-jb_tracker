import pandas as pd
import matplotlib.pyplot as plt

day_hour_df = pd.read_csv(r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\sorted_data.csv")

cols = []
rows = []
for index, row in day_hour_df.iterrows():
    col = f'0{index}-00'
    cols.append(col[-5:])
    values_sum = row.sum()
    rows.append(round(values_sum, 2))
    print(col, values_sum)


# Create a figure and axis
fig, ax = plt.subplots(figsize=(24, 2))

# Hide axes
ax.axis('off')

# Add the table to the plot
table = ax.table(cellText=[rows], colLabels=cols, loc='center')
# Color the header (first row)
for (i, j), cell in table.get_celld().items():
    if i == 0:  # Set the background color of the header row
        cell.set_fontsize(14)
        cell.set_text_props(weight='bold')
        cell.set_facecolor('#D3D3D3')  # Light grey color for header
# Display the plot
plt.show()

