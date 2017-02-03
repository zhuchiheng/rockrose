"""
Multi-threads and pygame.

TODO:
* Lock

"""

import random
import time

import threading
import Queue

import pygm
import consts


class PgThrd(threading.Thread):
    """
    Thread for PyGame.

    Note:
      1. You should overwrite the do_once() method;
      2. All the external threads should be putted in the main PyGame
         class with method thrd_add().
    """
    def __init__(self, q=None, slpt=0.1, *args, **kwargs):
        super(PgThrd, self).__init__()

        self.q = q

        self.slpt = slpt
        self.stopped = False

    def run(self):
        while not self.stopped:
            slpt = self.do_once()
            if slpt is None:
                slpt = self.slpt
            time.sleep(slpt)

    def stop(self):
        self.stopped = True

    def do_once(self):
        pass
