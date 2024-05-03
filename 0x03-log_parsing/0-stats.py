#!/usr/bin/python3
"""Log parsing"""


import sys
import re


def verify_log_entry(log_entry):
    """Verify if the log entry matches the specified format"""
    fp = (
        r"\s*(?P<ip>\S+)\s*",
        r"\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]",
        r'\s*"(?P<request>[^"]*)"\s*',
        r"\s*(?P<status_code>\S+)",
        r"\s*(?P<file_size>\d+)",
    )
    info = {
        "status_code": 0,
        "file_size": 0,
    }
    log_fmt = "{}\\-{}{}{}{}\\s*".format(fp[0], fp[1], fp[2], fp[3], fp[4])
    resp_match = re.fullmatch(log_fmt, log_entry)
    if resp_match is not None:
        status_code = resp_match.group("status_code")
        file_size = int(resp_match.group("file_size"))
        info["status_code"] = status_code
        info["file_size"] = file_size
    return info


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
        for line in sys.stdin:
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
