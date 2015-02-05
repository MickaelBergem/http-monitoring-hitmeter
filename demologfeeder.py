#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
from datetime import datetime
import config
from display import Display


if __name__ == '__main__':
    # TODO: argument handling
    logfile_path = '/tmp/demo.log'
    delay = 8  # (seconds)
    buffer_size = 1  # Line buffered

    with open(logfile_path, 'a', buffer_size) as file:
        while(True):
            file.write('127.0.0.1 - - [23/Jul/2014:20:09:28 +0200] "GET /section1/ HTTP/1.1" 200 1004 "-" "curl/7.32.0" "Apache/2.4.6 (Linux/SUSE) OpenSSL/1.0.1h"\n')
            time.sleep(delay)
