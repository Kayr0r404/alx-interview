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


def print_dict(dictionary) -> None:
    """print dictionary"""
    for key, val in dictionary.items():
        if val == 0:
            continue
        print(f"{key}: {val}")


def stats_computation():
    """reads stdin line by line and computes metrics:"""
    counter, file_size = 1, 0

    dict_of_status_code = {
        "200": 0,
        "301": 0,
        "400": 0,
        "401": 0,
        "403": 0,
        "404": 0,
        "405": 0,
        "500": 0,
    }
    for line in sys.stdin:

        if verify_log_entry(line):
            if counter == 11:
                counter = 0
                print(f"File size: {file_size}")
                print_dict(dict_of_status_code)
            counter += 1
            file_size += int(line.rstrip().split()[-1])
            status_code = line.rstrip().split()[-2]
            if status_code in dict_of_status_code.keys():
                dict_of_status_code[status_code] += 1


def main():
    """main func"""
    stats_computation()


if __name__ == "__main__":
    main()
