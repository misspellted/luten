
from ..stages.base import Stage
from ..scenes.base import Scene

class Act: # It really is one! ... _cough_ ...
  def __init__(self):
    self.stage:Stage = None
    self.scenes:list[Scene] = []
    self.current = None
    self.ended = False

  def next(self):
    if 0 == len(self.scenes):
      self.end()
    else:
      self.stage.clear()
      self.current = self.scenes.pop(0)
      self.current.open(self.stage)

  def open(self, stage:Stage):
    """
    Opens the act on the stage.
    """
    self.stage = stage
    self.next()

  def end(self):
    """
    Ends the act on the stage.
    """
    self.ended = True

  def update(self, delta_nanos:int) -> bool:
    """
    Updates the act.

    Indicates whether or not the act ended during or as a result of the update.
    """
    if not self.ended and None != self.current:
      if self.current.update(delta_nanos):
        self.next()

    return self.ended
