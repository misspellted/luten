
from .base import Act, Stage

class Greet(Act):
  def __init__(self):
    Act.__init__(self)

  def open(self, stage:Stage):
    stage.print("Hello, World!")
