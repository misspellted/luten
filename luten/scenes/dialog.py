
from .base import Scene, Stage

import logging

class Dialog(Scene):
  INTERVAL_TYPING = 1_000_000 * 50 # ms

  def __init__(self, viewer_dialog:bool, text:str, delay_ns:int):
    Scene.__init__(self)
    self.viewer_dialog:bool = viewer_dialog
    self.cooldown = delay_ns
    self.text:str = text
    self.padding:tuple[int, int] = (1, 1)
    self.dialog_rect:tuple[int, int, int, int] = None
    self.cooldown_typing:int = Dialog.INTERVAL_TYPING
    self.text_rect:tuple[int, int, int, int] = None
    self.characters_remaining:str = len(text)

  def open(self, stage:Stage) -> bool:
    if not Scene.open(self, stage):
      return False # An early exit is preferred here, avoiding the extra indent.

    self.stage.hide_cursor()

    columns, rows = self.stage.dimensions
    stage_rect = (0, 0, columns - 1, rows - 1)

    logging.debug(f"Stage rectangle: {stage_rect}")

    dialog_dimensions = (max(1, columns // 2), max(1, rows // 4)) # Might get cramped, depending on the invoking terminal dimensions or a terribly sized emulated terminal.
    
    if self.viewer_dialog:
      self.dialog_rect = (stage_rect[2] - self.padding[0] - dialog_dimensions[0], stage_rect[3] - self.padding[1] - dialog_dimensions[1], stage_rect[2] - self.padding[0], stage_rect[3] - self.padding[1])
    else:
      self.dialog_rect = (stage_rect[0] + self.padding[0], stage_rect[1] + self.padding[1], dialog_dimensions[0], dialog_dimensions[1])

    # Set the text rectangle inset of the dialog box.
    self.text_rect = (self.dialog_rect[0] + 1, self.dialog_rect[1] + 1, self.dialog_rect[2] - 1, self.dialog_rect[3] - 1)

    logging.debug(f"Dialog rectangle: {self.dialog_rect}")

    # Corners
    self.stage[(self.dialog_rect[0], self.dialog_rect[1])] = (ord("."), 7, 0)
    self.stage[(self.dialog_rect[2], self.dialog_rect[1])] = (ord("."), 7, 0)
    self.stage[(self.dialog_rect[2], self.dialog_rect[3])] = (ord("*"), 7, 0)
    self.stage[(self.dialog_rect[0], self.dialog_rect[3])] = (ord("*"), 7, 0)

    # Top border
    for _ in range(self.dialog_rect[0] + 1, self.dialog_rect[2], 1):
      self.stage[(_, self.dialog_rect[1])] = (ord("-"), 7, 0)
    # Right border
    for _ in range(self.dialog_rect[1] + 1, self.dialog_rect[3], 1):
      self.stage[(self.dialog_rect[2], _)] = (ord("|"), 7, 0)
    # Bottom border
    for _ in range(self.dialog_rect[2] - 1, self.dialog_rect[0], -1):
      self.stage[(_, self.dialog_rect[3])] = (ord("_"), 7, 0)
    # Left border
    for _ in range(self.dialog_rect[3] - 1, self.dialog_rect[1], -1):
      self.stage[(self.dialog_rect[0], _)] = (ord("|"), 7, 0)

    return True

  def update(self, delta_nanos:int) -> bool:
    ending = self.characters_remaining <= 0 and self.cooldown <= 0

    if not ending:
      typing = 0 < self.characters_remaining

      if typing:
        self.cooldown_typing -= delta_nanos

        if self.cooldown_typing <= 0:
          self.cooldown_typing = Dialog.INTERVAL_TYPING
          self.characters_remaining -= 1

          next_char = (self.text_rect[0], self.text_rect[1])

          # Display already displayed characters.
          logging.debug(f"Typing cooldown: {self.cooldown_typing}")
          logging.debug(f"Displaying {len(self.text) - self.characters_remaining} character(s): {self.text[:-self.characters_remaining]}")
          for _ in range(len(self.text) - self.characters_remaining):
            logging.debug(f"Setting '{self.text[_]}' at {next_char} in {self.text_rect}")
            self.stage[next_char] = (ord(self.text[_]), 7, 0)

            # It's basically a mini-terminal area.. there's a chance for a refactor/abstraction! YAY!
            nc, nr = next_char

            nc += 1

            if self.text_rect[2] <= nc:
              nc = self.text_rect[0]
              nr += 1
            
              if self.text_rect[3] <= nr:
                nr -= 1 # TODO: Scroll text up a line.

            next_char = (nc, nr)

      else:
        self.cooldown -= delta_nanos

    return ending
