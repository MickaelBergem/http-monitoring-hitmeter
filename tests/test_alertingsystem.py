import unittest
import time
from alertingsystem import AlertingSystem


class AlertingSystemTest(unittest.TestCase):

    base_time = int(time.time())
    alert_state_timed_hits = {
        base_time-1: 50,
        base_time-20: 90,
        base_time-60: 40,
        base_time-80: 15,
    }
    ok_state_timed_hits = {
        base_time-1: 80,
        base_time-20: 15,
        base_time-60: 110,
        base_time-80: 50,
    }

    def setUp(self):
        # Threshold : 100 hits for 30 seconds
        self.alerting_system = AlertingSystem(100, 30)

    def test_get_number_of_hits(self):

        self.alerting_system.timed_hits = self.alert_state_timed_hits

        hits = self.alerting_system.get_number_of_hits()

        self.assertEqual(hits, 140)

    def test_check_for_alert(self):

        self.alerting_system.check_for_alert()
        self.assertEqual(len(self.alerting_system.messages), 0)

        # Ok state
        self.alerting_system.timed_hits = self.ok_state_timed_hits

        self.assertEqual(
            self.alerting_system.check_for_alert(),
            False,
        )
        self.assertEqual(len(self.alerting_system.messages), 0)

        # Alert state
        self.alerting_system.timed_hits = self.alert_state_timed_hits
        self.assertEqual(
            self.alerting_system.check_for_alert(),
            True,
        )
        self.assertEqual(self.alerting_system.is_alerting, True)
        self.assertEqual(self.alerting_system.hit_number, 140)
        self.assertEqual(len(self.alerting_system.messages), 1)

        self.alerting_system.check_for_alert()
        self.assertEqual(len(self.alerting_system.messages), 1)

        # Recovery state
        self.alerting_system.timed_hits = self.ok_state_timed_hits
        self.assertEqual(
            self.alerting_system.check_for_alert(),
            False,
        )
        self.assertEqual(len(self.alerting_system.messages), 2)
