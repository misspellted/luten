

from .base import Act, Stage
from ..scenes.dialog import Dialog, Scene

class Shop(Act):
  def __init__(self, opening_dialog:list[tuple[bool, str, int]]):
    self.scenes:list[Scene] = [Dialog(viewer, text, delay_ns) for viewer, text, delay_ns in opening_dialog] # Nice!
    self.current = -1
    self.stage:Stage = None

  def open(self, stage:Stage):
    self.stage = stage

    if 0 < len(self.scenes):
      self.current = 0
      self.scenes[self.current].open(stage)

  def update(self, delta_nanos:int) -> bool:
    ended = 0 == len(self.scenes)

    if not ended:
      ended = self.scenes[self.current].ended
      self.current += 1 if ended else 0

      if ended and self.current < len(self.scenes):
        ended = False # There are more Scenes to this Act!
        self.stage.clear()
        self.scenes[self.current].open(self.stage)

      if not ended:
        self.scenes[self.current].on_update(delta_nanos)

    return ended
