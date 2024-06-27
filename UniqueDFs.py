
import os

# Get the list of rune names
rune_names = df['rune_name'].unique()

# Create a directory for the rune data
directory = '/content/drive/MyDrive/BitcoinRunes'
if not os.path.exists(directory):
    os.makedirs(directory)

# Iterate through each rune name
for rune_name in rune_names:
    # Filter the DataFrame for the current rune
    rune_df = df[df['rune_name'] == rune_name]

    # Create a filename for the rune
    filename = os.path.join(directory, f'{rune_name}.csv')

    # Save the rune data to a CSV file
    rune_df.to_csv(filename, index=False
