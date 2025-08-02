
from .terminal import Terminal

import pygame, string, logging

class PyGameTerm(Terminal):
  """
  An 8-color, Pygame-based stage for emulating terminal-like clients.
  """
  COLORS = {
    0x0: (0x00, 0x00, 0x00),
    0x1: (0xAA, 0x00, 0x00),
    0x2: (0x00, 0xAA, 0x00),
    0x3: (0xAA, 0x55, 0x00),
    0x4: (0x00, 0x00, 0xAA),
    0x5: (0x00, 0xAA, 0xAA),
    0x6: (0x00, 0xAA, 0xAA),
    0x7: (0xAA, 0xAA, 0xAA),
  }

  def __init__(self, columns:int, rows:int, font_name:str="dejavusansmono", font_size:int=20, sys_font:bool=True):
    Terminal.__init__(self, columns, rows)
    pygame.init()
    self.window:pygame.Surface = None
    self.font:pygame.Font = pygame.font.SysFont(font_name, font_size) if sys_font else pygame.font.Font(font_name, font_size)
    self.cell:pygame.Rect = None
    self.cursor_visible:bool = True # Start with the cursor shown.

    if 0 < (columns * rows) and 0 < columns: # The product of two negative values produces a positive value.
      # Get the actual character box for all the printable characters.
      # (Since font_size:20 could see characters having 15, 23, 24, and 26 heights, depending on font_name).
      longest, tallest = (0, 0)

      for character in string.printable:
        cs = self.font.size(character)
        longest = max(longest, cs[0])
        tallest = max(tallest, cs[1])

      self.cell = pygame.Rect(0, 0, longest, tallest)
      self.window = pygame.display.set_mode((columns * self.cell.width, rows * self.cell.height))
      logging.debug(f"[PyGameTerm::__init__] - emulating {(columns, rows)} (characters) with window of {self.window.get_size()} (pixels)")

  def refresh(self):
    # logging.debug(f"PyGameTerm::refresh() - windows is set? {None != self.window}")
    nanos = self.on_refresh_debut()

    # print("\x1b[2J", end="") # Not needed.
    # print("\x1b[H", end="") # The view is always refreshed with a new buffer:

    if None != self.window:
      buffer = pygame.Surface(self.window.get_size())

      for row in range(self.dimensions[1]):
        for column in range(self.dimensions[0]):
          c, f, b = self[(column, row)]
          # logging.debug(f"PyGameTerm::refresh() - c: {c}; f: {f}; b: {b}")
          # print(f"\x1b[{30 + f};{40 + b}m{chr(c)}", end="")

          background = PyGameTerm.COLORS[b]
          foreground = PyGameTerm.COLORS[f]
          # print(background, foreground)

          cell = pygame.Surface(self.cell.size)
          cell.fill(background)

          char = self.font.render(chr(c), True, foreground, background)

          # # char may have a smaller rectangle than self.cell.
          # # If this occurs, right and top align the char.
          # xoff = cell.get_width() - char.get_width()
          # xoff = 0 if xoff < 0 else xoff
          # cell.blit(char, (xoff, 0)) # Can't tell if this one..
          cell.blit(char) # .. or this one is better.
          buffer.blit(cell, (column * self.cell.width, row * self.cell.height))

          if (column, row) == self.cursor.position and self.cursor_visible:
            cursor = self.font.render("_", True, foreground, background)
            buffer.blit(cursor, (column * self.cell.width, row * self.cell.height)) #, special_flags=pygame.BLEND_RGB_ADD)

        # if row < self.dimensions[1] - 1: # And this can be ignored as well.
        #   print()
      
      self.window.blit(buffer)
      pygame.display.flip()
    
    # This looks weird, but since the time in nanoseconds should use the same reference, eh.. gud 'nuf *dismissive hand waves*...
    self.on_refresh_arret(self.on_refresh_debut() - nanos)

  def show_cursor(self):
    # print("\x1b[?25h", end="")
    self.cursor_visible = True

  def hide_cursor(self):
    # print("\x1b[?25l", end="")
    self.cursor_visible = False

  def exit(self):
    # self.show_cursor() # Not necessary in the emulated version.
    # print("\x1b[0m") # Same.
    pygame.quit()
