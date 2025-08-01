
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.invoking import Invoking
from luten.theaters.piegame import Emulated
from luten.acts.greet import Greet
from luten.acts.csi import CSI
from luten.acts.rain import Rain # This Act on the integrated terminal (Bash) on Arch Linux is slightly better (less updates, less warn for flashing lights, but still ... "glitchy-like" feeling).
from luten.acts.stripes import Stripes # The integrated terminal (Bash) on Arch Linux doesn't like this Act. Very much warn for flashing lights.

# theater = Invoking()
theater = Emulated(80, 25)

# One-Shot Acts
# --------------------------------
# theater.perform(Greet())
# theater.perform(CSI())

# Note: These one-shot acts don't do so great on emulation (they close very quickly).

# Updated Acts
# --------------------------------
# theater.perform(Stripes(250, 1)) # Limit to 250 updates; don't want it acting forever!
theater.perform(Rain(250)) # Limit to 250 updates; don't want it acting forever!

theater.start()
