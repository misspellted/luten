
from .base import Act, Stage

import logging

class Stripes(Act):
  ROLLING_INTERVAL = 1_000_000 * 16 # ms

  def __init__(self, max_updates:int, rolling:int=0):
    Act.__init__(self)
    self.rolling = rolling
    self.rolled = 0
    self.cooldown = Stripes.ROLLING_INTERVAL
    self.remaining_updates:int = max_updates
    self.stage:Stage = None

  def open(self, stage:Stage):
    self.stage = stage
    self.stage.hide_cursor()

    columns, rows = stage.dimensions

    for row in range(rows):
      for column in range(columns):
        stage[(column, row)] = (ord(" "), 0, column & 0x7) # You can feel the slowness on the opening...

  def update(self, delta_nanos:int) -> bool:
    self.remaining_updates -= 1
    # logging.debug(f"Remaining updates: {self.remaining_updates}")

    if 0 < self.rolling:
      self.cooldown -= delta_nanos

      if self.cooldown <= 0:
        self.cooldown = Stripes.ROLLING_INTERVAL
        self.rolled += self.rolling

        columns, rows = self.stage.dimensions

        for row in range(rows):
          for column in range(columns):
            c = (column + self.rolled) % columns
            self.stage[(column, row)] = (ord(" "), 0, c & 0x7)

    return self.remaining_updates == 0
