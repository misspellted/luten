
import time

class Stage:
  """
  A stage on which an act is played.
  """
  def __init__(self, dimensions:tuple):
    self.axes:int = 0
    self.dimensions:tuple = None

    self.on_resize(dimensions)

  def on_resize(self, dimensions:tuple):
    self.axes = len(dimensions)

    if 0 < self.axes:
      self.dimensions = tuple(dimensions)

  def on_refresh_debut(self) -> int:
    """
    Provides a notification to generate the start time in nanoseconds before a refresh is performed.
    """
    return time.time_ns()

  def on_refresh_arret(self, refresh_nanos:int):
    """
    Provides a notification for the time elapsed in nanoseconds to perform the refresh.
    """
    pass

  def refresh(self):
    """
    Refreshes the stage (output) to the viewer.
    """
    pass

  def exit(self):
    """
    Ends the performance.
    """
    pass
