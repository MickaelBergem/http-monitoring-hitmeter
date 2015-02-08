"""
Monitor

The monitor represents the state of the application
"""
import re
import config
from alertingsystem import AlertingSystem


class HttpMonitor(object):
    """ The state of the application """

    w3clogformat = re.compile(r'\A(?P<remoteHost>\S+) (?P<rfc931>\S+) (?P<authUser>\S+) \[(?P<date>[^\]]+)\] "(?P<rawRequest>[^"]*)" (?P<status>\d+) (?P<bytes>\S+)')

    requestformat = re.compile(r'(?P<method>\S+) (?P<request>(\*|/(?P<section>[^/]*)/(\S*)?|/(\S*)?)) (?P<protocol>[^ ]+)?')

    def __init__(self, logfile_stream, cumulative=False,
                 alert_threshold=config.DEFAULT_THRESHOLD,
                 alert_delay=config.DEFAULT_DELAY):
        self.logfile_stream = logfile_stream

        self.cumulative = cumulative

        self.sections_hits = {}
        self.total_hits = 0
        self.total_errors = 0

        self.alerting_system = AlertingSystem(alert_threshold, alert_delay)

        # Initial processing
        self._process_logs()

    def update(self):
        """ Update the metrics """

        # Reset the sections hits counter if the cumulative mode is disabled
        if not self.cumulative:
            self.reset_sections_hits()

        self._process_logs()
        self.alerting_system.check_for_alert()

    def reset_sections_hits(self):
        """ Reset the sections hits counter """
        self.sections_hits = {section: 0 for section in self.sections_hits}

    def get_hits_rate(self, period=60):
        """ Get the number of hits of the last 60s """
        return self.alerting_system.get_number_of_hits(period)

    def _process_logs(self):
        """ Process all the new lines since the last update """
        new_hits = 0

        for log_line in self.logfile_stream:
            parsed_data = self._parse_log_entry(log_line)

            self.total_hits += 1
            new_hits += 1

            if not parsed_data['well-formed']:
                # Not able to understand this log entry : not an error hit, but nothing more
                continue

            if parsed_data['status'][0:1] in ['4', '5']:
                # "Failure" entry
                self.total_errors += 1

            # We log the section anyway
            section = parsed_data['section']

            if section not in self.sections_hits:
                self.sections_hits[section] = 0
            self.sections_hits[section] += 1

        # Update the traffic for the alerting system
        self.alerting_system.update_traffic_stat(new_hits)

    def _parse_log_entry(self, entry):
        """ Parse a single log entry and returns interesting information """

        parsed_data = self.w3clogformat.match(entry)

        if not parsed_data:
            print("Found an invalid log entry : %s" % entry)
            return {'well-formed': False}

        # Parse the raw request
        parsed_request = self.requestformat.match(parsed_data.group('rawRequest'))

        if not parsed_request:
            print("Found an invalid request field for log entry : %s" % parsed_data.group('rawRequest'))
            return {'well-formed': False}

        return {
            'method': parsed_request.group('method'),
            'section': parsed_request.group('section'),
            'status': parsed_data.group('status'),
            'well-formed': True,
        }
