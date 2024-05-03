#!/usr/bin/python3
"""Log parsing"""


import sys
import re


def verify_log_entry(log_entry):
    """Verify if the log entry matches the specified format"""
    fp = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)'
    )
    info = {
        'status_code': 0,
        'file_size': 0,
    }
    log_fmt = '{}\\-{}{}{}{}\\s*'.format(fp[0], fp[1], fp[2], fp[3], fp[4])
    resp_match = re.fullmatch(log_fmt, input_line)
    if resp_match is not None:
        status_code = resp_match.group('status_code')
        file_size = int(resp_match.group('file_size'))
        info['status_code'] = status_code
        info['file_size'] = file_size
    return info


def output_format(file_size, status_code_counts):
    """Print the computed metrics"""
    print(f"Total file size: {file_size}")
    for code in sorted(status_code_counts):
        if status_code_counts[code] > 0:
            print(f"{code}: {status_code_counts[code]}")


def update_metrics(line, total_file_size, status_codes_stats):
    """Updates the metrics from a given HTTP request log.

    Args:
        line (str): The line of input from which to retrieve the metrics.

    Returns:
        int: The new total file size.
    """
    line_info = verify_log_entry(line)
    status_code = line_info.get("status_code", "0")
    if status_code in status_codes_stats.keys():
        status_codes_stats[status_code] += 1
    return total_file_size + line_info["file_size"]


def run():
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
    run()

# def run_stats_computation():
#     """Read stdin line by line and compute metrics"""
#     counter = 0
#     total_file_size = 0
#     status_code_counts = {
#         "200": 0,
#         "301": 0,
#         "400": 0,
#         "401": 0,
#         "403": 0,
#         "404": 0,
#         "405": 0,
#         "500": 0,
#     }

#     try:
#         for line in sys.stdin:

#             line_info = verify_log_entry(line)
#             status_code = line_info.get("status_code", "0")
#             if status_code in status_code_counts.keys():
#                 status_code_counts[status_code] += 1

#             total_file_size += line_info.get("file_size", "0")
#             counter += 1
#             if counter % 10 == 0:
#                 output_format(total_file_size, status_code_counts)
#     except (KeyboardInterrupt, EOFError):
#         output_format(total_file_size, status_code_counts)


# if __name__ == "__main__":
#     run_stats_computation()
