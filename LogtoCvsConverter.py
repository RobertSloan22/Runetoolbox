import csv
import re

# Define the log file and the output CSV file
log_file = 'app.log'
csv_file = 'app.csv'

# Regular expression to parse the log lines
log_pattern = re.compile(r'^(?P<timestamp>[\d-]+\s[\d:,]+):(?P<level>\w+):(?P<message>.*)$')

# Open the log file and the CSV file
with open(log_file, 'r') as lf, open(csv_file, 'w', newline='') as cf:
	csv_writer = csv.writer(cf)
	# Write the header row
	csv_writer.writerow(['Timestamp', 'Level', 'Message'])
	
	# Read and parse each line in the log file
	for line in lf:
		match = log_pattern.match(line)
		if match:
			timestamp = match.group('timestamp')
			level = match.group('level')
			message = match.group('message')
			# Write the parsed data to the CSV file
			csv_writer.writerow([timestamp, level, message])
