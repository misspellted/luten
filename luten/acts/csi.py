
from .base import Act, Stage

class CSI(Act):
  COOLDOWN = 1_000_000 * 1_000 # ms

  def __init__(self):
    Act.__init__(self)
    self.stage:Stage = None
    self.cooldown = CSI.COOLDOWN

  def open(self, stage:Stage):
    self.stage = stage
    self.stage.hide_cursor()

    for color in range(8):
      stage.print(f"\x1b[3{color}mHello, \x1b[7mWorld!\x1b[m\n\r")

  def end(self):
    self.stage.show_cursor()
    Act.end(self)

  def update(self, delta_nanos:int) -> bool:
    self.cooldown -= delta_nanos

    return self.cooldown <= 0
