#!/usr/bin/python3
"""Log parsing"""


import sys
import re


def verify_log_entry(log_entry):
    """Verify if the log entry matches the specified format"""
    # Define the regex pattern to match the specified format
    pattern = (
        r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) - \[([0-9]+-[0-9]+-[0-9]+ "
        r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+)\] "GET /projects/260 HTTP/1\.1" '
        r"([0-9]+) ([0-9]+)"
    )
    # Use re.match to check if the log entry matches the pattern
    match = re.match(pattern, log_entry)
    if match:
        status_code = match.group(3)
        file_size = int(match.group(4))
    return {"status_code": status_code, "file_size": file_size}


def output_format(file_size, status_code_counts):
    """Print the computed metrics"""
    print(f"Total file size: {file_size}")
    for code in sorted(status_code_counts):
        if status_code_counts[code] > 0:
            print(f"{code}: {status_code_counts[code]}")


def run_stats_computation():
    """Read stdin line by line and compute metrics"""
    counter = 0
    total_file_size = 0
    status_code_counts = {
        "200": 0,
        "301": 0,
        "400": 0,
        "401": 0,
        "403": 0,
        "404": 0,
        "405": 0,
        "500": 0,
    }

    try:
        for line in sys.stdin:

            line_info = verify_log_entry(line)
            status_code = line_info.get("status_code", "0")
            if status_code in status_code_counts.keys():
                status_code_counts[status_code] += 1
            # total_file_size + line_info['file_size']

            total_file_size += line_info.get("file_size", "0")
            counter += 1
            if counter % 10 == 0:
                output_format(total_file_size, status_code_counts)
    except (KeyboardInterrupt, EOFError):
        output_format(total_file_size, status_code_counts)


if __name__ == "__main__":
    run_stats_computation()
