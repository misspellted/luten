
from .base import Act, Stage

import logging

class Stripes(Act):
  COOLDOWN = 1_000_000 * 500 # ms
  ROLLING_INTERVAL = 1_000_000 * 33 # ms

  def __init__(self, max_updates:int, rolling:int=0):
    Act.__init__(self)
    self.stage:Stage = None
    self.cooldown = Stripes.COOLDOWN
    self.rolling = rolling
    self.rolled = 0
    self.cooldown_rolling = Stripes.ROLLING_INTERVAL
    self.updates_remaining:int = max_updates

  def open(self, stage:Stage):
    self.stage = stage
    self.stage.hide_cursor()

    columns, rows = stage.dimensions

    for row in range(rows):
      for column in range(columns):
        stage[(column, row)] = (ord(" "), 0, column & 0x7) # You can feel the slowness on the opening...

  def end(self):
    self.stage.show_cursor()
    Act.end(self)

  def update(self, delta_nanos:int) -> bool:
    ending = self.updates_remaining <= 0 and self.cooldown <= 0

    if not ending:
      rolling = 0 < self.rolling and 0 < self.updates_remaining
      # logging.debug(f"Remaining updates: {self.updates_remaining}")

      if rolling:
        self.cooldown_rolling -= delta_nanos

        if self.cooldown_rolling <= 0:
          self.cooldown_rolling = Stripes.ROLLING_INTERVAL
          self.rolled += self.rolling
          self.updates_remaining -= 1

          columns, rows = self.stage.dimensions

          for column in range(columns):
            for row in range(rows):
              c = (column + self.rolled) % columns
              self.stage[(column, row)] = (ord(" "), 0, c & 0x7)

      else:
        self.cooldown -= delta_nanos

    return ending
