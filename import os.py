import os

input_file = 'C:\\Users\\merki10p\\Documents\\Habits Heart rate test file\\heart_rate-2024-08-26.json'

# Check if the file exists before trying to open it
if os.path.exists(input_file):
    print(f"File exists: {input_file}")
else:
    print(f"File not found: {input_file}")
    exit()

# Proceed with the rest of your code if the file exists
