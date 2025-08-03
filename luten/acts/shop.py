

from .base import Act, Stage
from ..scenes.dialog import Dialog, Scene

class Shop(Act):
  def __init__(self, opening_dialog:list[tuple[bool, str, int]]):
    Act.__init__(self)
    self.scenes.extend([Dialog(viewer, text, delay_ns) for viewer, text, delay_ns in opening_dialog]) # Nice!
