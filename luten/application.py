
from .clients.base import Client as Application

class Display:
  def refresh(self):
    pass

class GraphicalApplication(Application):
  """
  An abstract extension of an Application adding an notification point to refresh the display.
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

from .scene import Scene

import pygame

class PyGameApp(GraphicalApplication):
  def __init__(self):
    GraphicalApplication.__init__(self)
    pygame.init()
    self.window:pygame.Surface = None
    self.scene:Scene = None

  @property
  def dimensions(self):
    return None if self.window == None else self.window.get_size()

  def open(self, length:int, height:int) -> bool:
    opened = 0 < (length * height) and 0 < length # If both length and height are negative, their product would be positive. So check one of the terms as well.

    if opened:
      self.window = pygame.display.set_mode((length, height))

    return opened

  def watch(self, scene:Scene):
    self.scene = scene

  def handle(self, event:pygame.Event):
    pass

  def process(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.stop(forced=True) # The user clicked on the X button to close the window, not using in-screen methods to exit, thus it is forced.
        break

  def refresh(self):
    if self.running and self.window != None and self.scene != None:
      self.window.blit(self.scene.capture())
      pygame.display.flip()

  def update(self, delta_nanos:int):
    if self.scene != None:
      self.scene.update(delta_nanos=delta_nanos)

    GraphicalApplication.update(self, delta_nanos=delta_nanos)

  def terminate(self):
    pygame.quit()
    self.window = None
