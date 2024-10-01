import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Load the data from your CSV file
input_file = r'W:\\HABITS\\habits fitbit data\\ha040mp_t2\\interpolated_hr_data_2024-08-28.csv'
df = pd.read_csv(input_file)

# Combine the 'Date' and 'Time' columns into a single datetime column
df['DateTime'] = pd.to_datetime(df['NZ Date'] + ' ' + df['NZ Time'], format='%Y-%m-%d %H:%M:%S')

# Convert HR (BPM) column to numeric, setting errors='coerce' to handle any blanks or 'NA' values
df['HR (BPM)'] = pd.to_numeric(df['HR (BPM)'], errors='coerce')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['DateTime'], df['HR (BPM)'], color='blue', marker='o', linestyle='-', markersize=2)

# Formatting the plot
plt.title('Heart Rate Over Time', fontsize=16, pad=30) # Add padding to title to prevent overlap
plt.xlabel('Time', fontsize=14)
plt.ylabel('Heart Rate (BPM)', fontsize=14)

# Format x-axis to show detailed time and only one date
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # Show time (hours, minutes, seconds)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Set major ticks for every hour
plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))  # Set minor ticks every 10 minutes

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add the date as a single label on top of the plot , positioned above the plot to avoid overlapping with the title
date_str = df['DateTime'].dt.date.unique()[0]  # Extract the date
plt.figtext(0.5, 0.92, f"Date: {date_str}", ha='center', fontsize=12, weight='bold')

# Use tight layout to improve spacing
plt.tight_layout()

# Extract the filename from the input file path
file_name = os.path.basename(input_file)

# Extract '24-08-27' from 'interpolated_hr_data_24-08-27.csv'
date_str = file_name.split('_')[3].split('.')[0]  # Get the date part (2024-08-27)

# Construct the output file name with the extracted date
output_file = os.path.join(os.path.dirname(input_file), f'heart_rate_plot_{date_str}.png')

# Save the plot
plt.savefig(output_file, bbox_inches='tight')  # Save the figure with tight layout to avoid clipping
plt.close()  # Close the figure to free up memory

print(f'Plot saved to {output_file}')
