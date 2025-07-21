
class Scene:
  def __init__(self):
    self.act = None

  def play(self, act):
    self.act = act

  def update(self, delta_nanos:int):
    pass

  def capture(self):
    pass

import pygame
import string

class PyGameTerm(Scene):
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
    if not pygame.get_init():
      pygame.init()
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
      self.dimensions = (self.columns * self.cell.width, self.rows * self.cell.height)
      self.reset()

  def reset(self):
    size = self.columns * self.rows
    self.attributes = [0x0F] * size # Default to black background and white foreground.
    self.characters = [0x20] * size # "Empty" ... space.
    self.cursor = (0, 0)

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

  def swap(self):
    if self.attributes != None:
      index = self.cursor[1] * self.columns + self.cursor[0]
      back_code = (self.attributes[index] & 0xF0)
      fore_code = self.attributes[index] & 0x0F
      self.attributes[index] = (fore_code << 4) | (back_code >> 4)

  def set_char(self, character:int):
    if self.characters != None:
      self.characters[self.cursor[1] * self.columns + self.cursor[0]] = ((ord(character) if isinstance(character, str) else character) & 0xFF)

  def set_pos(self, column:int, row:int):
    if self.cursor != None and 0 <= column < self.columns and 0 <= row < self.rows:
      self.cursor = (column, row)

  def advance(self):
    if self.cursor != None:
      column, row = self.cursor
      attributes = self.attributes[row * self.columns + column]
      column += 1

      if self.columns <= column:
        row += 1
        column = 0
      
      if self.rows <= row:
        row = 0 # Wrap around (TODO: Shift lines up).

    self.cursor = (column, row)
    self.attributes[row * self.columns + column] = attributes

  def update(self, delta_nanos:int):
    if self.act != None:
      self.act.update(delta_nanos=delta_nanos)

  def capture(self):
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
    
    return buffer
