"""
Display manager
"""
import curses


class Display(object):
    """ Display manager """

    def __init__(self, monitor):
        # Attach the monitor
        self.monitor = monitor
        # Draw the screen a first time
        self.screen = curses.initscr()
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

        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(1, 2, "Total hits : %d \t Total errors : %d" %
                           (self.monitor.total_hits, self.monitor.total_errors))

        # We want to order the sections by their number of hits
        section_hits = sorted(self.monitor.sections_hits.items(),
                              key=lambda item: item[1],
                              reverse=True)

        # Display each section with its hits number
        section_line_number = 4
        for section, hits in section_hits:
            self.screen.addstr(section_line_number, 4,
                               "%d  \t%s" % (hits, section))
            section_line_number += 1

        self.screen.refresh()
