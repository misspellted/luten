
from .base import Act, Stage

class Stripes(Act):
  # ROLLING_INTERVAL = 1_000_000 * 16 # ms

  def __init__(self): #, rolling:int=0):
    Act.__init__(self)
  #   self.rolling = rolling
  #   self.rolled = 0
  #   self.cooldown = Stripes.ROLLING_INTERVAL

  def open(self, stage:Stage):
    columns, rows = stage.dimensions

    for row in range(rows):
      for column in range(columns):
        stage[(column, row)] = (ord(" "), 0, column & 0x7) # You can feel the slowness on the opening...

  # def update(self, delta_nanos:int) -> bool:
  #   if 0 < self.rolling:
  #     self.cooldown -= delta_nanos
  #     if self.cooldown <= 0:
  #       self.cooldown = Stripes.ROLLING_INTERVAL
  #       self.rolled += self.rolling

  #       for row in range(self.scene.rows):
  #         for column in range(self.scene.columns):
  #           c = (column + self.rolled) % self.scene.columns
  #           self.scene.set_back((row * self.scene.columns + c) & 0xF)
  #           self.scene.advance()
