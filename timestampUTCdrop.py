import pandas as pd

# Load the data from a CSV file
df = pd.read_csv('/content/drive/MyDrive/NovakCryptoWork/cat_df.csv')

# Assign the loaded DataFrame to a variable
final_data = df.copy()

# Convert the 'timestamp' column to datetime, handling various formats
final_data['timestamp'] = pd.to_datetime(final_data['timestamp'], errors='coerce')

# Remove milliseconds and timezone from the 'timestamp' column
final_data['timestamp'] = final_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Set the 'timestamp' column as the index of the DataFrame
final_data.set_index('timestamp', inplace=True)

# Print the final DataFrame to verify the result
print(final_data)
