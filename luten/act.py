
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

class Rainbow(Act):
  ROLLING_INTERVAL = 1_000_000 * 16 # ms

  def __init__(self, scene, rolling:int=0):
    Act.__init__(self, scene)
    self.rolling = rolling
    self.rolled = 0
    self.scene.hidden = True
    self.cooldown = Rainbow.ROLLING_INTERVAL

    for row in range(self.scene.rows):
      for column in range(self.scene.columns):
        self.scene.set_back((row * self.scene.columns + column) & 0xF)
        self.scene.advance()

  def update(self, delta_nanos:int):
    if 0 < self.rolling:
      self.cooldown -= delta_nanos
      if self.cooldown <= 0:
        self.cooldown = Rainbow.ROLLING_INTERVAL
        self.rolled += self.rolling

        for row in range(self.scene.rows):
          for column in range(self.scene.columns):
            c = (column + self.rolled) % self.scene.columns
            self.scene.set_back((row * self.scene.columns + c) & 0xF)
            self.scene.advance()
