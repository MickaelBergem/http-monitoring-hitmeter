import unittest
import datetime
from alerts import Alert


class AlertTest(unittest.TestCase):
    def test_alert_class(self):

        alert1 = Alert(100)
        self.assertEqual(alert1.hit_number, 100)
        self.assertIsInstance(alert1.time_alert, datetime.datetime)
        self.assertEqual(
            alert1.message,
            'High traffic generated an alert - hits = 100, triggered at %s'
             % alert1.time_alert.strftime('%H:%m (%d/%m)')
        )

        alert2 = Alert(50, recovery=True,
                       last_alert_time=alert1.time_alert + datetime.timedelta(seconds=-150))
        self.assertEqual(alert2.hit_number, 50)
        self.assertIsInstance(alert2.time_alert, datetime.datetime)
        self.assertEqual(
            alert2.message,
            'Alert recovered after 2 minute(s) and 30 second(s), hits are now 50, triggered at %s'
            % alert2.time_alert.strftime('%H:%m (%d/%m)')
        )
