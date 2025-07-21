
class Act: # It really is one! ... _cough_ ...
  def __init__(self, scene):
    self.scene = scene

  def update(self, delta_nanos:int):
    pass

class Greeting(Act):
  def __init__(self, scene):
    Act.__init__(self, scene)

    # "Amber"...-ish terminal..
    self.scene.set_fore(0x06)

    # For testing, the traditional is only fair.
    motd = bytes("Hello, World!", "UTF-8")
    for i in range(len(motd)):
      self.scene.set_char(motd[i])
      self.scene.advance()
      self.scene.swap()

      # BUG: The background is filled on the cell, blitted to the buffer, and then the background is filled on cursor, blitted with blending to buffer, causing higher intensity.

class Stripes(Act):
  ROLLING_INTERVAL = 1_000_000 * 16 # ms

  def __init__(self, scene, rolling:int=0):
    Act.__init__(self, scene)
    self.rolling = rolling
    self.rolled = 0
    self.scene.hidden = True
    self.cooldown = Stripes.ROLLING_INTERVAL

    for row in range(self.scene.rows):
      for column in range(self.scene.columns):
        self.scene.set_back((row * self.scene.columns + column) & 0xF)
        self.scene.advance()

  def update(self, delta_nanos:int):
    if 0 < self.rolling:
      self.cooldown -= delta_nanos
      if self.cooldown <= 0:
        self.cooldown = Stripes.ROLLING_INTERVAL
        self.rolled += self.rolling

        for row in range(self.scene.rows):
          for column in range(self.scene.columns):
            c = (column + self.rolled) % self.scene.columns
            self.scene.set_back((row * self.scene.columns + c) & 0xF)
            self.scene.advance()

import random

class Rain(Act):
  FALL_INTERVAL = 1_000_000 * 16 # ms
  DROP_INTERVAL = 1_000_000 * 33 # ms # TODO: Make this more variable?

  def __init__(self, scene):
    Act.__init__(self, scene)
    self.drops = list() # (col, row)
    self.max_drops = 10
    self.fall_cooldown = Rain.FALL_INTERVAL
    self.drop_cooldown = Rain.DROP_INTERVAL

  def update(self, delta_nanos:int):
    self.fall_cooldown -= delta_nanos

    if self.fall_cooldown <= 0:
      self.fall_cooldown = Rain.FALL_INTERVAL

      # First, update positions of any current drops.
      falling = list()

      for _ in range(len(self.drops)):
        column, row = self.drops.pop(0)

        # First clear the current position.
        self.scene.set_pos(column, row)
        self.scene.set_char(" ")
        self.scene.set_back(0)
        self.scene.set_fore(0)

        # Update the position.
        row += 1

        # If the drop didn't collide with the "ground" last update, then it is still falling (even if it collides this update).
        if row < self.scene.rows:
          falling.append((column, row))
        # Otherwise, the ground absorbed the rain... (ignoring it)

      self.drops.extend(falling)
      falling.clear()

    # Then spawn new drops.
    self.drop_cooldown -= delta_nanos

    if len(self.drops) < self.max_drops and self.drop_cooldown <= 0:
      self.drop_cooldown = Rain.DROP_INTERVAL

      # Spawn a drop in an unoccupied cell.
      position = None
      occupied = True
      while occupied:
        position = (random.randrange(0, self.scene.columns), random.randrange(0, self.scene.rows // 2)) # Start in the upper-half of the terminal.
        occupied = position in self.drops

      self.drops.append(position)

    # Update the view.
    for position in self.drops:
      self.scene.set_pos(*position)
      self.scene.set_char("*")
      self.scene.set_back(1)
      self.scene.set_fore(7)
