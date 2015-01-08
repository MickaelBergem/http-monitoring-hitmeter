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
            file.write("It is %s !\n" % datetime.now())
            time.sleep(delay)
