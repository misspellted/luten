
import time

class Application:
  """
  An abstract application based on a simple loop.
  """

  def __init__(self):
    self.running:bool = False
    self.nanos:int = 0

  def process(self):
    """
    Processes events, such as user input or platform notifications.
    """
    pass

  def on_delta(self, delta_nanos:int):
    pass

  def update(self, delta_nanos:int):
    """
    Updates the application state, after processing events.
    """
    pass

  def terminate(self):
    """
    Provides the application a chance to clean up resources after the simple
    loop exits, prior to process termination.
    """
    pass

  def stop(self, forced:bool):
    """
    Sets the flag to stop the simple loop.
    """
    self.running = False

    if not forced:
      self.terminate()

  def start(self):
    """
    Starts the simple loop.
    """
    self.running = True
    self.nanos = time.time_ns()

    while self.running:
      self.process()

      if self.running:
        nanos = time.time_ns()
        delta, self.nanos = nanos - self.nanos, nanos
        self.on_delta(delta_nanos=delta)
        self.update(delta_nanos=delta)

    self.stop(forced=False)

class GraphicalApplication(Application):
  """
  An abstract extension of the application adding an notification point to refresh the display.
  """
  def __init__(self):
    Application.__init__(self)

  def refresh(self):
    """
    Refreshes the display visible to the user.
    """
    pass

  def update(self, delta_nanos:int):
    """
    By default, only calls the refresh() method to update the display.

    Any graphical-related updates required by the application should be performed prior to this call executing.
    For example, an overriding class could override GraphicalApplication::update(), performing all the graphical
      updates, then finishing with calling the overridden GraphicalApplication::update() which will update the
      display.
    """
    if self.running:
      self.refresh()

import pygame

class PyGameApp(GraphicalApplication):
  def __init__(self):
    GraphicalApplication.__init__(self)
    pygame.init()
    self.window:pygame.Surface = None

  @property
  def dimensions(self):
    return None if self.window == None else self.window.get_size()

  def open(self, length:int, height:int) -> bool:
    opened = 0 < (length * height) and 0 < length # If both length and height are negative, their product would be positive. So check one of the terms as well.

    if opened:
      self.window = pygame.display.set_mode((length, height))

    return opened

  def handle(self, event:pygame.Event):
    pass

  def process(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.stop(forced=True) # The user clicked on the X button to close the window, not using in-screen methods to exit, thus it is forced.
        break

  def refresh(self):
    if self.window != None:
      pygame.display.flip()

  def terminate(self):
    pygame.quit()
    self.window = None

import string

class PyGameTerm(PyGameApp):
  COLORS = {
    0x0: (0x00, 0x00, 0x00),
    0x1: (0x00, 0x00, 0xAA),
    0x2: (0x00, 0xAA, 0x00),
    0x3: (0x00, 0xAA, 0xAA),
    0x4: (0xAA, 0x00, 0x00),
    0x5: (0xAA, 0x00, 0xAA),
    0x6: (0xAA, 0x55, 0x00),
    0x7: (0xAA, 0xAA, 0xAA),
    0x8: (0x55, 0x55, 0x55),
    0x9: (0x55, 0x55, 0xFF),
    0xA: (0x55, 0xFF, 0x55),
    0xB: (0x55, 0xFF, 0xFF),
    0xC: (0xFF, 0x55, 0x55),
    0xD: (0xFF, 0x55, 0xFF),
    0xE: (0xFF, 0xFF, 0x55),
    0xF: (0xFF, 0xFF, 0xFF),
  }

  def __init__(self, columns:int=80, rows:int=25, font_name:str="dejavusansmono", font_size:int=20, sys_font:bool=True):
    PyGameApp.__init__(self)
    self.columns:int = columns
    self.rows:int = rows
    self.font:pygame.Font = pygame.font.SysFont(font_name, font_size) if sys_font else pygame.font.Font(font_name, font_size)
    self.cell:pygame.Rect = None
    self.attributes:list[int] = None
    self.characters:list[int] = None
    self.cursor:tuple[int, int] = None
    self.hidden:bool = False

    if 0 < (columns * rows):
      # Get the actual character box for all the printable characters.
      # (Since font_size:20 could see characters having 15, 23, 24, and 26 heights, depending on font_name).
      longest, tallest = (0, 0)

      for character in string.printable:
        cs = self.font.size(character)
        longest = max(longest, cs[0])
        tallest = max(tallest, cs[1])

      self.cell = pygame.Rect(0, 0, longest, tallest)
      
      # Now a window can be opened.
      if self.open(self.columns * self.cell.width, self.rows * self.cell.height):
        self.reset()
        self.cursor = (0, 0)

  def reset(self):
    size = self.columns * self.rows
    self.attributes = [0x0F] * size # Default to black background and white foreground.
    self.characters = [0x20] * size # "Empty" ... space.

  def ready(self):
    return self.cursor != None

  def set_back(self, color_code:int):
    if self.attributes != None:
      index = self.cursor[1] * self.columns + self.cursor[0]
      fore_code = self.attributes[index] & 0x0F
      self.attributes[index] = ((color_code & 0x0F) << 4) | fore_code

  def set_fore(self, color_code:int):
    if self.attributes != None:
      index = self.cursor[1] * self.columns + self.cursor[0]
      back_code = (self.attributes[index] & 0xF0)
      self.attributes[index] = back_code | (color_code & 0x0F)

  def set_char(self, character:int):
    if self.characters != None:
      self.characters[self.cursor[1] * self.columns + self.cursor[0]] = (character & 0xFF)

  def set_pos(self, column:int, row:int):
    if self.cursor != None and 0 <= column < self.columns and 0 <= row < self.rows:
      self.cursor = (column, row)

  def advance(self):
    if self.cursor != None:
      column, row = self.cursor
      column += 1

      if self.columns <= column:
        row += 1
        column = 0
      
      if self.rows <= row:
        row = 0 # Wrap around (TODO: Shift lines up).

    self.cursor = (column, row)

  def refresh(self):
    if self.running and self.ready():
      buffer = pygame.Surface(self.dimensions)
      
      for row in range(self.rows):
        for column in range(self.columns):
          index = row * self.columns + column
          attribute = self.attributes[index]
          character = self.characters[index]

          background = PyGameTerm.COLORS[(attribute & 0xF0) >> 4]
          foreground = PyGameTerm.COLORS[attribute & 0x0F]
          # print(background, foreground)

          cell = pygame.Surface(self.cell.size)
          cell.fill(background)

          char = self.font.render(chr(character), True, foreground, background)

          # # char may have a smaller rectangle than self.cell.
          # # If this occurs, right and top align the char.
          # xoff = cell.get_width() - char.get_width()
          # xoff = 0 if xoff < 0 else xoff
          # cell.blit(char, (xoff, 0)) # Can't tell if this one..
          cell.blit(char) # .. or this one is better.
          buffer.blit(cell, (column * self.cell.width, row * self.cell.height))

          if (column, row) == self.cursor and not self.hidden:
            cursor = self.font.render("_", True, foreground, background)
            buffer.blit(cursor, (column * self.cell.width, row * self.cell.height), special_flags=pygame.BLEND_RGB_ADD)

      self.window.blit(buffer)

    PyGameApp.refresh(self)
