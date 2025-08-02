
from ..stages.base import Stage

class Scene:
  def __init__(self):
    self.ended = False

  def open(self, stage:Stage):
    """
    Opens the scene on the stage.
    """
    pass

  def end(self): # "End scene!"
    """
    Ends the scene on the stage.
    """
    self.ended = True

  def on_update(self, delta_nanos:int):
    """
    Updates the state of the scene without having to report a quitting state.
    """
    pass

  def update(self, delta_nanos:int) -> bool:
    """
    Updates the state of the scene.

    Indicates whether or not the update resulted in a quitting state.
    """
    self.on_update(delta_nanos)

    return self.ended
