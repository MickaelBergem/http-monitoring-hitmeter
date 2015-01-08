#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
import config
from display import Display


if __name__ == '__main__':
    # TODO: argument handling
    logfile_path = '/var/log/demo.log'

    try:
        # Initialize the console "display"
        display = Display()

        while True:
            display.update()
            time.sleep(config.DELAY_REFRESH_SCREEN)

    except KeyboardInterrupt:
        print("Exiting...")
