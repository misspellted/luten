
from .base import Act, Stage

import logging, random

class Rain(Act):
  FALL_INTERVAL = 1_000_000 * 16 # ms
  DROP_INTERVAL = 1_000_000 * 33 # ms # TODO: Make this more variable?

  def __init__(self, max_updates:int):
    Act.__init__(self)
    self.stage:Stage = None
    self.drops:list[tuple[int, int]] = list() # (col, row)
    self.max_drops:int = 10
    self.fall_cooldown:int = Rain.FALL_INTERVAL
    self.drop_cooldown:int = Rain.DROP_INTERVAL
    self.remaining_updates:int = max_updates

  def open(self, stage:Stage):
    self.stage = stage
    self.stage.hide_cursor()

  def update(self, delta_nanos:int) -> bool:
    self.remaining_updates -= 1
    logging.debug(f"Remaining updates: {self.remaining_updates}")

    self.fall_cooldown -= delta_nanos
    self.drop_cooldown -= delta_nanos

    columns, rows = self.stage.dimensions

    if self.fall_cooldown <= 0:
      self.fall_cooldown = Rain.FALL_INTERVAL

      # First, update positions of any current drops.
      falling = list()

      for _ in range(len(self.drops)):
        column, row = self.drops.pop(0)

        # First clear the current position.
        self.stage[(column, row)] = (ord(" "), 0, 0)

        # Update the position.
        row += 1

        # If the drop didn't collide with the "ground" last update, then it is still falling (even if it collides this update).
        if row < rows:
          falling.append((column, row))
        # Otherwise, the ground absorbed the rain... (ignoring it)

      self.drops.extend(falling)
      falling.clear()

    # Then spawn new drops.
    if len(self.drops) < self.max_drops and self.drop_cooldown <= 0:
      self.drop_cooldown = Rain.DROP_INTERVAL

      # Spawn a drop in an unoccupied cell.
      position = None
      occupied = True
      while occupied:
        position = (random.randrange(0, columns), random.randrange(0, rows // 2)) # Start in the upper-half of the terminal.
        occupied = position in self.drops

      self.drops.append(position)

    # Update the view.
    logging.debug(f"{len(self.drops)} drop(s) to display...")
    for position in self.drops:
      logging.debug(f"Drop at {position}")
      self.stage[position] = (ord("*"), 7, 4)
  
    return self.remaining_updates == 0
