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

        self.is_alerting = False

    def check_for_alert(self):
        """ Check if a threshold has been hit """
        hit_number = self._get_number_of_hits()

        if hit_number >= self.alert_threshold:
            self.is_alerting = True
            self.hit_number = hit_number
        else:
            self.is_alerting = False

        return self.is_alerting

    def update_traffic_stat(self, new_hits):
        """ Update the `timed_hits` variable to keep track of the evolution
            of the traffic and raise an alert if needed """

        block_time = int(time.time())
        self.timed_hits[block_time] = new_hits

        # TODO: clean the old blocks

    def _get_number_of_hits(self):
        """ Returns the number of hits during the last `alert_delay` seconds """
        current_time = time.time()
        return sum([
            hits
            for timestamp, hits in self.timed_hits.iteritems()
            if timestamp + self.alert_delay > current_time
        ])
