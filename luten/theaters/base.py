
from ..acts.base import Act

import time

class Theater:
  """
  A facility hosting a stage to perform acts.
  """

  def __init__(self):
    self.running:bool = False
    self.nanos:int = 0

  def perform(self, act:Act):
    """
    Performs an act on the stage.
    """
    pass

  def process(self):
    """
    Processes events, such as user input or platform notifications.
    """
    pass

  def update(self, delta_nanos:int) -> bool:
    """
    Updates the state of the theater after event processing, including refreshing the stage.

    Returns whether or not the update resulted in a quit condition.
    """
    pass

  def curtain(self):
    """
    Provides a chance to clean up resources prior to process termination.
    """
    pass

  def stop(self, forced:bool):
    self.running = False

    if not forced:
      self.curtain()

  def start(self):
    self.running = True
    self.nanos = time.time_ns()

    while self.running:
      self.process()

      if self.running:
        nanos = time.time_ns()
        delta, self.nanos = nanos - self.nanos, nanos
        self.running = not self.update(delta_nanos=delta)

    self.stop(forced=False)
