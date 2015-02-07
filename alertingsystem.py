"""
Alerting system

The alerting system keeps track of traffic peaks and raise alerts if needed
"""
import time


class AlertingSystem(object):
    """ Raise alerts in case of traffic peaks """

    def __init__(self, alert_threshold, alert_delay):

        self.alert_delay = alert_delay
        self.alert_threshold = alert_threshold

        # For traffic analysis
        self.timed_hits = {}

    def _check_for_alert(self):
        pass

    def update_traffic_stat(self, new_hits):
        """ Update the `timed_hits` variable to keep track of the evolution
            of the traffic and raise an alert if needed """

        block_time = int(time.time())
        self.timed_hits[block_time] = new_hits
