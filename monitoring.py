#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
import config
from display import Display
from httpmonitor import HttpMonitor


if __name__ == '__main__':
    # TODO: argument handling
    logfile_path = '/tmp/demo.log'

    with open(logfile_path, 'r') as logfile_stream:

        # Initialize the monitor
        monitor = HttpMonitor(logfile_stream)

        # Initialize the console "display"
        display = Display(monitor)

        # Main loop
        while True:
            try:
                monitor.update()
                display.update()
                time.sleep(config.DELAY_REFRESH_SCREEN)

            except KeyboardInterrupt:
                print("Exiting...")
                break
