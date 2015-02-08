import datetime


class Alert(object):
    """ An alert """

    def __init__(self, hit_number, time_alert=None,
                 recovery=False, last_alert_time=None):
        self.hit_number = hit_number
        self.time_alert = time_alert or datetime.datetime.now()
        self.recovery = recovery
        self._last_alert_time = last_alert_time

    @property
    def message(self):
        if self.recovery:
            alert_duration = self.time_alert - self._last_alert_time
            message = "Alert recovered after %s, hits are now %d" % (self._format_time(alert_duration.total_seconds()), self.hit_number)
        else:
            message = "High traffic generated an alert - hits = %d" % self.hit_number

        return "%s %s" \
            % (self.time_alert.strftime('[%d/%m %H:%M:%S]'), message)

    def _format_time(self, seconds):
        """ Returns a human-friendly time """
        if seconds <= 1:
            return "%d second" % seconds
        if seconds < 60:
            return "%d seconds" % seconds
        if seconds < 60*5:
            return "%d minute(s) and %d second(s)" % (seconds / 60, seconds % 60)

        return "%d minutes" % seconds/60
