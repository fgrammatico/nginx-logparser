import os
import glob
import re
import csv
from datetime import datetime
from tqdm import tqdm

# Function to parse timestamp
def parse_timestamp(timestamp_str, format_str):
    return datetime.strptime(timestamp_str, format_str).strftime('%Y%m%d%H%M%S')

# Function to get user input for directories
def get_directory_input(prompt):
    while True:
        directory = input(prompt)
        if os.path.isdir(directory):
            return directory
        else:
            print("Invalid directory. Please try again.")

# Get log directory from user
log_dir = get_directory_input("Enter the directory where Nginx logs are stored: ")

# Define log file paths
access_stream_logs = glob.glob(os.path.join(log_dir, "access-stream.log"))
error_logs = glob.glob(os.path.join(log_dir, "error.log"))

# Debug prints to check if files are found
print(f"Looking for access-stream logs in: {os.path.join(log_dir, 'access-stream.log')}")
print(f"Found access-stream logs: {access_stream_logs}")
print(f"Looking for error logs in: {os.path.join(log_dir, 'error.log')}")
print(f"Found error logs: {error_logs}")

# Regex patterns for log parsing
access_stream_pattern = re.compile(r'(?P<source_ip>\d+\.\d+\.\d+\.\d+) \[(?P<timestamp>[^\]]+)\] TCP (?P<status>\d{3}) (?P<size_req>\d+) (?P<size_resp>\d+) \d+\.\d+ \"(?P<upstream_ip>\d+\.\d+\.\d+\.\d+:\d+)\"')
error_pattern = re.compile(r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] \d+#\d+: \*(?P<request_id>\d+) (?P<error_message>.+?), client: (?P<source_ip>\d+\.\d+\.\d+\.\d+), server: [^,]+, upstream: "(?P<upstream_ip>[^"]+)",')

# Data storage
data = []

try:
    # Parse access-stream logs
    for log_file in tqdm(access_stream_logs, desc="Processing access-stream logs"):
        with open(log_file, 'rb') as file:
            for line in file:
                line = line.decode('utf-8', errors='ignore')
                match = access_stream_pattern.search(line)
                if match:
                    source_ip = match.group('source_ip')
                    timestamp = parse_timestamp(match.group('timestamp'), "%d/%b/%Y:%H:%M:%S %z")
                    upstream_ip = match.group('upstream_ip')
                    size_req = int(match.group('size_req'))
                    size_resp = int(match.group('size_resp'))
                    status = int(match.group('status'))

                    data.append((timestamp, source_ip, upstream_ip, size_req, size_resp, status, ""))

    # Parse error logs
    for log_file in tqdm(error_logs, desc="Processing error logs"):
        with open(log_file, 'rb') as file:
            for line in file:
                line = line.decode('utf-8', errors='ignore')
                match = error_pattern.search(line)
                if match:
                    timestamp = parse_timestamp(match.group('timestamp'), "%Y/%m/%d %H:%M:%S")
                    error_message = match.group('error_message')
                    level = match.group('level')
                    request_id = match.group('request_id')
                    source_ip = match.group('source_ip')
                    upstream_ip = match.group('upstream_ip')

                    data.append((timestamp, source_ip, upstream_ip, 0, 0, 0, f"{level}: {error_message}"))

    # Output data to CSV
    output_file_path = os.path.join(os.getcwd(), 'combined_data.csv')
    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['Timestamp', 'SourceIP', 'UpstreamIP', 'SizeReq', 'SizeResp', 'Status', 'ErrorDescription'])
        
        # Write data
        for entry in data:
            csvwriter.writerow(entry)

    print(f"Data extraction complete. Combined data saved to {output_file_path}.")

except Exception as e:
    print(f"An error occurred: {e}")
    raise