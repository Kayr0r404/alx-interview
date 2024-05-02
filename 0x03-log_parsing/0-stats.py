#!/usr/bin/python3
"""adsda"""
import sys
import re
from collections import defaultdict


def parse_log_line(line):
    # Regular expression to match the log line format
    pattern = (
        r'^(\d+\.\d+\.\d+\.\d+) - \[(.*?)\] "GET /projects/260 HTTP/1.1" (\d+) (\d+)$'
    )
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        status_code = int(match.group(3))
        file_size = int(match.group(4))
        return ip_address, status_code, file_size
    else:
        return None


def print_metrics(total_file_size, status_code_counts):
    print(f"Total file size: {total_file_size}")
    for code in sorted(status_code_counts.keys()):
        print(f"{code}: {status_code_counts[code]}")


def main():
    total_file_size = 0
    status_code_counts = defaultdict(int)
    line_count = 0

    try:
        for line in sys.stdin:
            line = line.strip()
            parsed = parse_log_line(line)
            if parsed:
                _, status_code, file_size = parsed
                total_file_size += file_size
                status_code_counts[status_code] += 1
                line_count += 1

            # Print metrics every 10 lines or upon interruption
            if line_count == 10:
                print_metrics(total_file_size, status_code_counts)
                line_count = 0

    except KeyboardInterrupt:
        # If interrupted by CTRL + C, print final metrics
        print_metrics(total_file_size, status_code_counts)


if __name__ == "__main__":
    main()
