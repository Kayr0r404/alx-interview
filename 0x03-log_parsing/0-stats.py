#!/usr/bin/python3
"""Log parsing"""


import sys
import re


def verify_log_entry(log_entry):
    """Verify if the log entry matches the specified format"""
    # Define the regex pattern to match the specified format
    pattern = (
        r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ - \[[0-9]+-[0-9]+-[0-9]+ "
        r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+\] "GET /projects/260 HTTP/1\.1" '
        r"([0-9]+) ([0-9]+)"
    )
    # Use re.match to check if the log entry matches the pattern
    match = re.match(pattern, log_entry)
    if match:
        file_size = int(log_entry.rstrip().split()[-1])
        status_code = log_entry.rstrip().split()[-2]
    return {"status_code": status_code, "file_size": file_size}


def output_format(total_file_size, status_codes_stats):
    """Print the computed metrics"""
    print("File size: {:d}".format(total_file_size), flush=True)
    for key, val in sorted(status_codes_stats.items()):
        if val > 0:
            print("{:s}: {:d}".format(key, val), flush=True)


def update_metrics(line, total_file_size, status_codes_stats):
    """Updates the metrics from a given HTTP request log."""
    line_info = verify_log_entry(line)
    status_code = line_info.get("status_code", "0")
    if status_code in status_codes_stats.keys():
        status_codes_stats[status_code] += 1
    return total_file_size + line_info["file_size"]


def run_stats_computations():
    """Starts the log parser."""
    line_num = 0
    total_file_size = 0
    status_codes_stats = {
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
        while True:
            line = input()
            total_file_size = update_metrics(
                line,
                total_file_size,
                status_codes_stats,
            )
            line_num += 1
            if line_num % 10 == 0:
                output_format(total_file_size, status_codes_stats)
    except (KeyboardInterrupt, EOFError):
        output_format(total_file_size, status_codes_stats)


if __name__ == "__main__":
    run_stats_computations()
