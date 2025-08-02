
from .base import Theater, Act
from ..stages.terminal import Terminal

import logging, os

class Invoking(Theater):
  """
  A theater utilizing the invoking terminal interface.
  """
  def __init__(self):
    Theater.__init__(self)
    dims = os.get_terminal_size()
    # logging.debug(dims)
    self.stage:Terminal = Terminal(*os.get_terminal_size())
    self.act:Act = None

  def perform(self, act:Act):
    if None != act:
      self.act = act
      self.act.open(self.stage)

  def process(self) -> bool:
    # TODO: Acquire user input via threaded input() calls.
    return False

  def update(self, delta_nanos:int) -> bool:
    quitting = False

    self.stage.refresh()

    if None != self.act:
      quitting = self.act.update(delta_nanos)
    
    return quitting

  def curtain(self):
    self.stage.exit()
