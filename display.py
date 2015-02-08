"""
Display manager
"""
import curses
import time


class Display(object):
    """ Display manager """

    def __init__(self, monitor):
        # Attach the monitor
        self.monitor = monitor
        # Draw the screen a first time
        self.time_start = time.time()
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.curs_set(0)  # Hide the cursor
        self._draw()

    def __del__(self):
        curses.endwin()

    def attach(self, monitor):
        """ Attach a given monitor to the display """
        self.monitor = monitor

    def update(self):
        """ Update the screen with the newest data """
        self._draw()

    def _draw(self):
        """ Draws the screen with the given data """

        # Line where sections and hits begin
        section_line_number = 4

        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(1, 2, "Total hits : %d" % self.monitor.total_hits)
        self.screen.addstr(2, 2, " Errors : %d (%d%%)"
                           % (self.monitor.total_errors, self.monitor.total_errors*100/self.monitor.total_hits))

        if self.monitor.alerting_system.is_alerting:
            self.screen.addstr(1, 35, "[ALERT !]", curses.color_pair(1))

        # Hit during the last minute, shows only after a minute of running
        if self.time_start + 60 < time.time():
            self.screen.addstr(3, 2, " Rate : %d hits/minute"
                               % self.monitor.get_hits_rate(60))
            section_line_number += 1

        # We want to order the sections by their number of hits
        section_hits = sorted(self.monitor.sections_hits.items(),
                              key=lambda item: item[1],
                              reverse=True)

        # Display each section with its hits number
        for section, hits in section_hits:
            self.screen.addstr(section_line_number, 4,
                               "%d  \t%s" % (hits, section))
            section_line_number += 1

        self._draw_alerts()

        self.screen.refresh()

    def _draw_alerts(self):
        """ Draws the alerts / messages """

        offset_y_alerts = 50

        # Header
        self.screen.addstr(1, offset_y_alerts-1, "%d message(s)"
                           % len(self.monitor.alerting_system.messages))

        line_number = 2
        for alert in reversed(self.monitor.alerting_system.messages):
            self.screen.addstr(line_number, offset_y_alerts, alert.message)
            line_number += 1 if alert.recovery else 2
