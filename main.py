
# from luten.application import PyGameApp
# from luten.scene import PyGameTerm
# from luten.act import Greeting, Stripes, Rain

import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

# app = PyGameApp()

# scn = PyGameTerm()

# if app.open(*scn.dimensions):
#   # scn.play(Greeting(scn))
#   # scn.play(Stripes(scn))
#   # scn.play(Stripes(scn, rolling=1))
#   scn.play(Rain(scn))

#   app.watch(scn)

#   try:
#     app.start()
#   except KeyboardInterrupt:
#     app.stop(forced=True)

# ================================

# I would like this to be the new style of performing acts.
# >> The above implementation was refactored prior to committing to the repo.
# At least until input can be captured in a non-blocking manner.

from luten.theaters.invoking import Invoking
# from luten.theaters.emulated import Emulated # TODO: Refactor PyGameApp/PyGameTerm above to emulate the terminal.
from luten.acts.greet import Greet
from luten.acts.csi import CSI
from luten.acts.rain import Rain
from luten.acts.stripes import Stripes

theater = Invoking()

# One-Shot Acts
# --------------------------------
# theater.perform(Greet())
# theater.perform(CSI())
theater.perform(Stripes())

# We'll reach into the theater to refresh the screen, as we cannot process input events just yet.
# theater.stage.refresh()

# Updated Acts
# --------------------------------
# theater.perform(Rain(250)) # Limit to 250 updates; don't want it raining forever!

theater.start()

theater.stage.exit()
