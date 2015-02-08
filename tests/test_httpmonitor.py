"""
Testing the HttpMonitor class


"""

import unittest
import time
from httpmonitor import HttpMonitor


class HttpMonitorTest(unittest.TestCase):

    def setUp(self):
        self.logfile_stream = open('tests/fixtures/example_apache.log', 'r')
        self.monitor = HttpMonitor(self.logfile_stream)

    def tearDown(self):
        self.logfile_stream.close()

    def test_parse_log_entry(self):

        self.assertEqual(
            self.monitor._parse_log_entry('not well formed')['well-formed'],
            False,
        )

        entry_1 = '::1 - - [27/Jun/2014:21:14:40 +0200] "GET /intranet/scripts/js/api.js HTTP/1.1" 304 - "http://localhost/intranet/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"'
        entry_1_parsed = self.monitor._parse_log_entry(entry_1)

        self.assertEqual(entry_1_parsed['well-formed'], True)
        self.assertEqual(entry_1_parsed['method'], 'GET')
        self.assertEqual(entry_1_parsed['section'], 'intranet')
        self.assertEqual(entry_1_parsed['status'], '304')

        entry_2 = '::1 - - [27/Jun/2014:21:14:40 +0200] "POST / HTTP/1.1" 200 34 "http://localhost/intranet/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"'
        entry_2_parsed = self.monitor._parse_log_entry(entry_2)

        self.assertEqual(entry_2_parsed['well-formed'], True)
        self.assertEqual(entry_2_parsed['method'], 'POST')
        self.assertEqual(entry_2_parsed['section'], None)
        self.assertEqual(entry_2_parsed['status'], '200')

    def test_process_logs(self):
        # Run the method
        self.monitor._process_logs()

        # Check the results
        self.assertEqual(self.monitor.total_hits, 13)
        self.assertEqual(self.monitor.total_errors, 3)

        # Check the sections hits
        self.assertEqual(
            self.monitor.sections_hits,
            {
                'test': 1,
                'phpMyAdmin': 1,
                None: 9,
                'intranet': 1
            }
        )

    def test_reset_hits(self):
        # Process
        self.monitor._process_logs()

        # Reset
        self.monitor.reset_sections_hits()
        for hits in self.monitor.sections_hits.values():
            self.assertEqual(hits, 0)

    def test_hit_rate(self):
        base_time = int(time.time())
        self.monitor.alerting_system.timed_hits = {
            base_time-1: 50,
            base_time-20: 90,
            base_time-50: 40,
            base_time-80: 15,
        }

        self.assertEqual(
            self.monitor.get_hits_rate(60),
            50+90+40
        )
