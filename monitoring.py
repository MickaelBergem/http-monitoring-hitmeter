#!/usr/bin/python3

"""
Monitoring tool written by Mickaël Bergem
"""
import time
import config
import argparse
from display import Display
from httpmonitor import HttpMonitor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Monitor a log file of HTTP access")
    parser.add_argument("logfile", help="Log file to monitor")
    # Monitoring settings
    parser.add_argument("--cumulative", dest='cumulative', action='store_true',
                        help="Always display all the hits,"
                             "not only the most recent")
    # Alerting system
    parser.add_argument("--alert-threshold", default=50,
                        help="Number of hits within the alert delay that will raise an alert")
    parser.add_argument("--alert-delay", default=2,
                        help="Number of minutes we need to watch the traffic for")
    args = parser.parse_args()

    with open(args.logfile, 'r') as logfile_stream:

        # Initialize the monitor
        monitor = HttpMonitor(logfile_stream, cumulative=args.cumulative)

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
