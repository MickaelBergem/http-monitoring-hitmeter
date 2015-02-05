"""
Display manager
"""


class Display(object):
    """ Display manager """

    def __init__(self, monitor):
        # Attach the monitor
        self.monitor = monitor
        # Draw the screen a first time
        self._draw()

    def attach(self, monitor):
        """ Attach a given monitor to the display """
        self.monitor = monitor

    def update(self):
        """ Update the screen with the newest data """
        self._draw()

    def _draw(self):
        print("Demo, hits=%d" % self.monitor.total_hits)
