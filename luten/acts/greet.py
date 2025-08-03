
from .base import Act, Stage

class Greet(Act):
  COOLDOWN = 1_000_000 * 500 # ms

  def __init__(self):
    Act.__init__(self)
    self.stage:Stage = None
    self.cooldown = Greet.COOLDOWN

  def open(self, stage:Stage):
    self.stage = stage
    self.stage.hide_cursor()

    stage.print("Hello, World!")

  def end(self):
    self.stage.show_cursor()
    Act.end(self)

  def update(self, delta_nanos:int) -> bool:
    self.cooldown -= delta_nanos

    return self.cooldown <= 0
