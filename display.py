"""
Display manager
"""


class Display(object):
    """ Display manager """

    def __init__(self):
        # Draw the screen a first time
        self._draw()

    def update(self):
        """ Update the screen with the newest data """
        self._draw()

    def _draw(self):
        print("Kikoo")
        pass
