
from ..stages.base import Stage

class Scene:
  def __init__(self):
    self.stage:Stage = None

  def open(self, stage:Stage) -> bool:
    """
    Opens the scene on the stage.

    Indicates whether or not the scene opened on the stage.
    """
    opened = isinstance(stage, Stage)

    if opened:
      self.stage = stage

    return opened

  def update(self, delta_nanos:int) -> bool:
    """
    Updates the scene.

    Indicates whether or not the scene ended during or as a result of the update.
    """
    return True
