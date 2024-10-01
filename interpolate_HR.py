import pandas as pd
import numpy as np
import os

# File paths
input_file = r'W:\\HABITS\\habits fitbit data\\ha040mp_t2\\output_2024-08-28.csv'
# temp_file = r'W:\\HABITS\\habits fitbit data\\ha040mp_t2\\temp_data.csv'

# Extract the date from the input filename
file_name = os.path.basename(input_file)

# Extract '2024-08-27' from 'output_2024-08-27.csv'
date_str = file_name.split('_')[1].split('.')[0]  # Get the date part (2024-08-27)

# Construct the output file name with the extracted date
output_file = f'W:\\HABITS\\habits fitbit data\\ha040mp_t2\\interpolated_hr_data_{date_str}.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Combine 'NZ Date' and 'NZ Time' columns into a single datetime column
df['DateTime'] = pd.to_datetime(df['NZ Date'] + ' ' + df['NZ Time'], format='%Y-%m-%d %H:%M:%S')

# Sort by 'DateTime' to ensure proper chronological order
df = df.sort_values(by='DateTime')

# Calculate time differences between consecutive rows
df['Time_Diff'] = df['DateTime'].diff(-1).dt.total_seconds()*-1

# Mark gaps where the time difference is greater than 60 seconds
df['Gap'] = df['Time_Diff'] > 60

# Save the interpolated DataFrame to a new CSV file (optional step)
# df.to_csv(temp_file, index=False)

# Create a full range of 1-second intervals from the minimum to maximum DateTime
full_range = pd.date_range(start=df['DateTime'].min(), end=df['DateTime'].max(), freq='1S')

# Reindex the DataFrame to the full range, filling with NaN
df_full = df.set_index('DateTime').reindex(full_range)

# Assign the new index as 'DateTime'
df_full.index.name = 'DateTime'

# Fill the 'Study ID' column with the first value of 'Study ID' across the entire reindexed DataFrame
df_full['Study ID'] = df['Study ID'].iloc[0]

# Forward fill the 'Gap' column, ensuring the 'Gap' marker is carried forward
df_full['Gap'] = df_full['Gap'].fillna(method='ffill')
#df_full.to_csv(temp_file, index=False)

# Interpolate only for non-gaps
df_full['HR (BPM)'] = df_full['HR (BPM)'].interpolate(method='linear')

# After interpolation, replace HR values in rows with gaps NaN
df_full.loc[df_full['Gap'] == True, 'HR (BPM)'] = np.nan  # Mark gaps as NaN
df_full['HR (BPM)'].fillna('NaN', inplace=True)  # Replace NaN with an empty string

# Reset index so that 'DateTime' becomes a column again
df_resampled = df_full.reset_index()

# Split 'DateTime' into separate 'NZ Date' and 'NZ Time'
df_resampled['NZ Date'] = df_resampled['DateTime'].dt.strftime('%Y-%m-%d')
df_resampled['NZ Time'] = df_resampled['DateTime'].dt.strftime('%H:%M:%S')

# Create a new DataFrame with the required columns
df_final = df_resampled[['Study ID', 'NZ Date', 'NZ Time', 'HR (BPM)']]

# Save the interpolated DataFrame to a new CSV file
df_final.to_csv(output_file, index=False)

print(f'Interpolated data saved to {output_file}')
