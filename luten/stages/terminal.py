
from .base import Stage

import logging, math

class TerminalCursor:
  def __init__(self):
    self.dimensions:tuple[int, int] = (0, 0)
    self.position = None
    self.previous = None

  def resize(self, columns:int, rows:int):
    ld, lp = self.dimensions, self.position

    size = columns * rows
    self.dimensions = (columns, rows) if 0 < size else (0, 0)
    self.position = (0, 0) if 0 < size else None

    # Ensure the old position is still within the new dimensions.
    if None not in [lp, self.position]:
      self.position = min(lp[0], self.dimensions[0]), min(lp[1], self.dimensions[1])

  def cursor_moved(self, delta_columns:int, delta_rows:int):
    pass

  def __check_cursor_moved(self):
    if None != self.position:
      if None == self.previous:
        self.cursor_moved(*self.position)
      else:
        dc, dr = self.position[0] - self.previous[0], self.position[1] - self.previous[1]
        # logging.debug(f"TerminalCursor::__check_cursor_moved() -> dc={dc}, dr={dr}")
        if 0 != dc or 0 != dr:
          self.cursor_moved(dc, dr)

  def on_line_feed(self):
    if self.position != None:
      self.previous = tuple(self.position)
      c, r = self.position
      r += 1

      if self.dimensions[1] <= r:
        r = self.dimensions[1] - 1
      
      self.position = (c, r)
      self.__check_cursor_moved()

  def on_carriage_return(self):
    if self.position != None:
      self.previous = tuple(self.position)
      self.position = (0, self.position[1])
      self.__check_cursor_moved()

  def advance(self):
    if self.position != None:
      self.previous = tuple(self.position)
      c, r = self.position

      c += 1

      if self.dimensions[0] <= c:
        c = 0
        r += 1

        if self.dimensions[1] <= r:
          r = self.dimensions[1] - 1
      
      self.position = (c, r)
      self.__check_cursor_moved()

  def to_offset(self, previous:bool=False) -> int:
    source = self.previous if previous else self.position
    return None if None == source else source[1] * self.dimensions[0] + source[0]

class Terminal(Stage):
  """
  An 8-color, character-based stage for terminal-like clients.
  """
  BG_DEFAULT = 0
  FG_DEFAULT = 7

  def __init__(self, columns:int, rows:int):
    Stage.__init__(self, (columns, rows))
    self.attributes:list[int] = None
    self.characters:list[int] = None
    self.cursor:TerminalCursor = TerminalCursor()

    if self.reset():
      self.cursor.cursor_moved = self.on_cursor_moved
      self.cursor.resize(*self.dimensions)
      logging.debug(f"[Terminal::__init__] - {(columns, rows)} (characters)")

  def reset(self) -> bool:
    size = math.prod(self.dimensions)

    if 0 < size:
      self.attributes = [(Terminal.BG_DEFAULT << 4) | Terminal.FG_DEFAULT] * size
      self.characters = [0x20] * size

    return 0 < size

  def on_cursor_moved(self, delta_columns:int, delta_rows:int):
    if None != self.attributes:
      # Copy the last attribute into the current attribute.
      offset = self.cursor.to_offset(previous=True)

      if None != offset:
        self.attributes[self.cursor.to_offset()] = self.attributes[offset]

  def __getitem__(self, coordinates:tuple[int, int]) -> tuple[int, int, int]:
    """
    Gets the attributed character at the specified coordinates (column, row).

    An attributed character is returned as an integer tuple of the character and foreground and background color codes [0-7].
    """
    if 2 != len(coordinates) or not (0 <= coordinates[0] and 0 <= coordinates[1]):
      raise ValueError("Check the provided coordinates for correctness.")
    
    offset = coordinates[1] * self.dimensions[0] + coordinates[0]
    attribute = self.attributes[offset]

    return (self.characters[offset], (attribute & 0x07), (attribute & 0x70) >> 4)

  def __setitem__(self, coordinates:tuple[int, int], character:tuple[int, int, int]):
    """
    Sets an attributed character at the specified coordinates (column, row).

    The attributed character is expected as an integer tuple of the character and foreground and background color codes [0-7].
    """
    if 2 != len(coordinates) or not (0 <= coordinates[0] and 0 <= coordinates[1]):
      raise ValueError("Check the provided coordinates for correctness.")
    
    offset = coordinates[1] * self.dimensions[0] + coordinates[0]

    if 3 != len(character) or not (0 <= character[1] < 8 and 0 <= character[2] < 8):
      raise ValueError("Check the provided character, foreground, or background values for correctness.")

    self.characters[offset] = character[0]
    self.attributes[offset] = ((character[2] & 0x7) << 4) | (character[1] & 0x7)

  def refresh(self):
    nanos = self.on_refresh_debut()

    print("\x1b[2J", end="")
    print("\x1b[H", end="")

    for row in range(self.dimensions[1]):
      for column in range(self.dimensions[0]):
        c, f, b = self[(column, row)]
        print(f"\x1b[{30 + f};{40 + b}m{chr(c)}", end="")
      if row < self.dimensions[1] - 1:
        print()
    
    # This looks weird, but since the time in nanoseconds should use the same reference, eh.. gud 'nuf *dismissive hand waves*...
    self.on_refresh_arret(self.on_refresh_debut() - nanos)

  def reset_attributes(self):
    # logging.debug("reset_attributes()")
    offset = self.cursor.to_offset()

    if None != offset:
      self.attributes[offset] = (Terminal.BG_DEFAULT << 4) | Terminal.FG_DEFAULT

  def set_foreground_color(self, color:int):
    # logging.debug(f"set_foreground_color({color}) @ {self.cursor.position}")
    offset = self.cursor.to_offset()

    if None != offset:
      previous = self.attributes[offset]
      updated = (previous & 0x70) | (color & 0x07)
      # logging.debug(f"set_foreground_color : attribute @ {self.cursor.position} : {previous:08b} -> {updated:08b}")
      self.attributes[offset] = updated

  def set_background_color(self, color:int):
    offset = self.cursor.to_offset()
    # logging.debug(f"set_background_color({color}) @ {self.cursor.position}")

    if None != offset:
      previous = self.attributes[offset]
      updated = ((color & 0x07) << 4) | (previous & 0x07)
      # logging.debug(f"set_background_color : attribute @ {self.cursor.position} : {previous:08b} -> {updated:08b}")
      self.attributes[offset] = updated

  def invert_colors(self):
    offset = self.cursor.to_offset()
    # logging.debug(f"invert_colors() @ {self.cursor.position}")

    if None != offset:
      attribute = self.attributes[offset]
      self.attributes[offset] = ((attribute & 0x07) << 4) | ((attribute & 0x70) >> 4)

  def on_select_graphic_redition(self, sgr:str):
    # logging.debug(f"on_select_graphic_redition({sgr})")

    # No attribtes converts to a reset all attributes (CSI 0 m).
    if 0 == len(sgr):
      self.reset_attributes()
    else:
      attributes = sgr.split(";")
      # logging.debug(f"on_select_graphic_redition : Length of attributes: {len(attributes)}")

      # Since certain attributes can have additional follow-up/on attributes, look-ahead is implemented here.
      for index in range(len(attributes)):
        attribute = attributes[index]
        # logging.debug(f"on_select_graphic_redition : attributes[{index}] = {attribute}")

        if attribute in [str(7)]:
          self.invert_colors()

        if attribute in [str(30 + _) for _ in range(8)]:
          self.set_foreground_color(int(attribute) - 30)

        elif attribute in [str(40 + _) for _ in range(8)]:
          self.set_background_color(int(attribute) - 40)

  def on_csi(self, csi:str):
    # logging.debug(f"on_csi({csi})")
    if csi[-1] == 'm':
      self.on_select_graphic_redition(csi[:-1])

  def print(self, text:str):
    # logging.debug(f"print({text}) [{self.cursor.position}]")
    if isinstance(text, str):
      index = 0
      while index < len(text):
        character = ord(text[index])
        index += 1

        # "Typewriter Control" Codes
        if 0x0a == character:
          self.cursor.on_line_feed()
        elif 0x0d == character:
          self.cursor.on_carriage_return()

        # ANSI Escape Sequences
        elif 0x1b == character:
          # Control Sequence Introducer
          # --------------------------------
          # Note: This only handles `\x1b[` CSI sequences, not the `\9b` CSI sequences.
          if 0x5b == ord(text[index]):
            index += 1
            csi = ""
            # Collect all parameter and intermediate bytes.
            while index < len(text) and 0x20 <= ord(text[index]) < 0x40:
              csi += text[index]
              index += 1
            # Finish the CSI with the final byte.
            if index < len(text) and 0x40 <= ord(text[index]) < 0x7F:
              csi += text[index]
              index += 1
              self.on_csi(csi)

        else:
          offset = self.cursor.to_offset()

          if None != offset:
            self.characters[offset] = character
            self.cursor.advance()
          else:
            break

  def show_cursor(self):
    print("\x1b[?25h", end="")

  def hide_cursor(self):
    print("\x1b[?25l", end="")

  def exit(self):
    self.show_cursor()
    print("\x1b[0m")
