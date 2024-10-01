import os
import json
from datetime import datetime, timedelta
import csv

input_file = 'C:\\Users\\merki10p\\Documents\\Habits Heart rate test file\\heart_rate-2024-08-26.json'
output_file = 'output.csv'

# Check if the file exists before trying to open it
if os.path.exists(input_file):
    print(f"File exists: {input_file}")
else:
    print(f"File not found: {input_file}")
    exit()

# Proceed with loading and processing the JSON file
try:
    with open(input_file, 'r') as f:
        json_data = json.load(f)
except json.JSONDecodeError:
    print("Error decoding JSON file.")
    exit()

# Define the start and end dates for NZST (Standard Time) in 2024
nzst_start = datetime(2024, 4, 7, 23, 59, 59)  # NZST starts on April 7, 2024, 23:59:59
nzst_end = datetime(2024, 9, 28, 23, 59, 59)   # NZST ends on September 28, 2024, 23:59:59

# Function to convert UTC to NZST/NZDT based on the date range
def convert_to_nzt(utc_datetime):
    if nzst_start <= utc_datetime <= nzst_end:
        # If the date is in NZST range, convert to UTC+12 (NZST)
        return utc_datetime + timedelta(hours=12)
    else:
        # Else, convert to UTC+13 (NZDT)
        return utc_datetime + timedelta(hours=13)

# Open the CSV file for writing
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Time', 'HR (BPM)', 'NZ Date', 'NZ Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each entry in the JSON data
    for entry in json_data:
        date_time_str = entry['dateTime']
        bpm = entry['value']['bpm']

        # Parse date and time in UTC
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')
        date = date_time_obj.strftime('%Y-%m-%d')
        time = date_time_obj.strftime('%H:%M:%S')

        # Convert UTC to NZST/NZDT based on the defined rules
        converted_nzt = convert_to_nzt(date_time_obj)
        nz_date = converted_nzt.strftime('%Y-%m-%d')  # Extract the converted date
        nz_time = converted_nzt.strftime('%H:%M:%S')  # Extract the converted time

        # Write the extracted information and the converted NZST/NZDT to separate columns
        writer.writerow({'Date': date, 'Time': time, 'HR (BPM)': bpm, 'NZ Date': nz_date, 'NZ Time': nz_time})

print(f'Data successfully written to {output_file}')




