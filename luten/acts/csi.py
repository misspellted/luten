
from .base import Act, Stage

class CSI(Act):
  def __init__(self):
    Act.__init__(self)

  def open(self, stage:Stage):
    for color in range(8):
      stage.print(f"\x1b[3{color}mHello, \x1b[7mWorld!\x1b[m\n\r")
