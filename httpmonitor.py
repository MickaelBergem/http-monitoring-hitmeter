"""
Monitor

The monitor represents the state of the application
"""
import re


class HttpMonitor(object):
    """ The state of the application """

    w3clogformat = re.compile(r'\A(?P<remoteHost>\S+) (?P<rfc931>\S+) (?P<authUser>\S+) \[(?P<date>[^\]]+)\] "(?P<rawRequest>[^"]*)" (?P<status>\d+) (?P<bytes>\S+)')

    requestformat = re.compile(r'(?P<method>\S+) (?P<request>(\*|/(?P<section>[^/]*)/(\S*)?|/(\S*)?)) (?P<protocol>[^ ]+)?')
    #(?P<method>\S+) (?P<request>/(?P<section>[^/]*)(?:/\S*)?(?P<protocol> \S+)?)

    def __init__(self, logfile_stream):
        self.logfile_stream = logfile_stream

        self.sections_hits = {}
        self.total_hits = 0
        self.total_errors = 0

    def update(self):
        """ Update the metrics """
        self._process_logs()

    def _process_logs(self):
        """ Process all the new lines since the last update """
        for log_line in self.logfile_stream:
            parsed_data = self._parse_log_entry(log_line)

            self.total_hits += 1

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

    def _parse_log_entry(self, entry):
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
