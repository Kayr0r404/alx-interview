#!/usr/bin/python3
"""Log parsing"""


import sys
import re


def verify_log_entry(log_entry):
    """verify the stdin format"""
    # Define the regex pattern to match the specified format
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)$'

    # Use re.match to check if the log entry matches the pattern
    match = re.match(pattern, log_entry)
    if match:
        return True
    return False


def stats():
    """reads stdin line by line and computes metrics:"""
    counter, file_size = 1, 0
    for line in sys.stdin:

        if verify_log_entry(line):
            if counter == 10:
                counter = 0
                print(f"File size: {file_size}")
            counter += 1
            file_size += int(line.rstrip().split()[-1])


def main():
    """main func"""
    stats()
