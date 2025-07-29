
from ..stages.base import Stage

class Act: # It really is one! ... _cough_ ...
  def __init__(self):
    pass

  def open(self, stage:Stage):
    """
    Opens the act on the stage.
    """
    pass

  def update(self, delta_nanos:int) -> bool:
    """
    Updates the state of the act.

    Indicates whether or not the update resulted in a quitting state.

    By default, returns True (simplifies 'one-shot' acts).
    """
    return True
