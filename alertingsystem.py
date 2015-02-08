"""
Alerting system

The alerting system keeps track of traffic peaks and raise alerts if needed
"""
import time
from alerts import Alert


class AlertingSystem(object):
    """ Raise alerts in case of traffic peaks """

    def __init__(self, alert_threshold, alert_delay):

        self.alert_delay = alert_delay
        self.alert_threshold = alert_threshold

        # For traffic analysis
        self.timed_hits = {}

        # Data
        self.is_alerting = False
        self.last_alert_time = None

        # Contains the list of the alerts
        self.messages = []

    def check_for_alert(self):
        """ Check if a threshold has been hit """
        hit_number = self._get_number_of_hits()

        if hit_number >= self.alert_threshold:
            if not self.is_alerting:
                # This is a NEW alert
                alert = Alert(hit_number)
                self.messages.append(alert)
                self.last_alert_time = alert.time_alert

            self.is_alerting = True
            self.hit_number = hit_number
        else:
            if self.is_alerting:
                # This is a NEW recovery
                self.messages.append(
                    Alert(
                        hit_number,
                        recovery=True,
                        last_alert_time=self.last_alert_time
                    )
                )

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
        current_time = int(time.time())
        return sum([
            hits
            for timestamp, hits in self.timed_hits.items()
            if timestamp + self.alert_delay > current_time
        ])
