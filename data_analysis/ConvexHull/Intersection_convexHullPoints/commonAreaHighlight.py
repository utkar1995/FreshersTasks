import numpy as np
import matplotlib.pyplot as plt

# Example set of random points
points = np.array([[1, 2], [4, 5], [6, 2], [7, 8], [3, 6], [9, 4]])

# Existing plot
plt.scatter(points[:, 0], points[:, 1], c='blue', label='Points')

# Create a polygon using the points
polygon = plt.Polygon(points, closed=True, edgecolor='green', facecolor='lightgreen')

# Get the current axis
ax = plt.gca()

# Add the polygon to the axis
ax.add_patch(polygon)

# Set axis labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Set title
ax.set_title('Polygon Added to Existing Plot')

# Display the updated plot
plt.show()

import pandas as pd

# Example dictionary with lists of different lengths
data_dict = {
    'Key1': [1, 2, 3],
    'Key2': [4, 5],
    'Key3': [6, 7, 8, 9]
}



# Find the maximum length among the lists
max_length = max(len(values) for values in data_dict.values())

# Fill lists with NaN to make them the same length
for key in data_dict:
    data_dict[key] += [float('nan')] * (max_length - len(data_dict[key]))

print(data_dict)
# Create a DataFrame from the modified dictionary
df_filled = pd.DataFrame(data_dict)

# Export the DataFrame to an Excel file
excel_file_path = 'data_filled.xlsx'  # Provide the desired file path
df_filled.to_excel(excel_file_path, index=False)


