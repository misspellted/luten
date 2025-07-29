
from .base import Theater, Act
from ..stages.piegame import PyGameTerm

import logging, os, pygame

class Emulated(Theater):
  """
  A theater utilizing the PyGame-based emulated terminal interface.
  """
  def __init__(self, columns:int, rows:int):
    Theater.__init__(self)
    logging.debug((columns, rows))
    self.stage:PyGameTerm = PyGameTerm(columns, rows)
    self.act:Act = None

  def perform(self, act:Act):
    if None != act:
      self.act = act
      self.act.open(self.stage)

  def process(self) -> bool:
    quitting = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quitting = True
        break
    
    return quitting

  def update(self, delta_nanos:int) -> bool:
    quitting = False

    self.stage.refresh()

    if None != self.act:
      quitting = self.act.update(delta_nanos)
    
    return quitting

  def curtain(self):
    self.stage.exit()
