#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
import random
from datetime import datetime
import config
from display import Display


if __name__ == '__main__':
    # TODO: argument handling
    logfile_path = '/tmp/demo.log'
    delay = 2  # (seconds)
    buffer_size = 1  # Line buffered

    http_response_codes = [200, 201, 204, 301, 400, 500]

    with open(logfile_path, 'a', buffer_size) as file:
        while(True):
            random_params = (random.randint(1, 5),
                             random.choice(http_response_codes))

            log_line = '127.0.0.1 - - [23/Jul/2014:20:09:28 +0200] "GET /section%d/ HTTP/1.1" %d 1004 "-" "curl/7.32.0" "Apache/2.4.6 (Linux/SUSE) OpenSSL/1.0.1h"\n' \
                % random_params

            print("Simulated request on /section%d/ with response code %d" % random_params)
            file.write(log_line)
            time.sleep(delay)
