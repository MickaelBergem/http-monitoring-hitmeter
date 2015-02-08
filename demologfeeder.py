#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
import random
import config
import argparse
from datetime import datetime
from lib.display import Display


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate random hits in a HTTP access log")
    parser.add_argument("logfile", help="Log file to write to")
    parser.add_argument("-d", "--delay", default=1,
                        help="Time to wait between to hits")
    args = parser.parse_args()
    logfile_path = args.logfile
    delay = float(args.delay)  # (seconds)
    buffer_size = 1  # Line buffered

    http_response_codes = [200, 201, 204, 301, 400, 500]

    with open(logfile_path, 'a', buffer_size) as file:
        while(True):
            random_params = (random.randint(1, 5),
                             random.choice(http_response_codes))

            log_line = '127.0.0.1 - - [23/Jul/2014:20:09:28 +0200] "GET /section%d/ HTTP/1.1" %d 1004 "-" "curl/7.32.0"\n' \
                % random_params

            print("Simulated request on /section%d/ with response code %d" % random_params)
            file.write(log_line)
            time.sleep(delay)
