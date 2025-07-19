
from luten.application import PyGameApp
from luten.scene import PyGameTerm
from luten.act import Greeting, Rainbow

import logging
logging.basicConfig(filename="luten.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

app = PyGameApp()
app.on_delta = lambda delta_nanos: logger.debug(f"delta_nanos {delta_nanos}")

scn = PyGameTerm()

if app.open(*scn.dimensions):
  scn.play(Greeting(scn))
  # scn.play(Rainbow(scn))
  # scn.play(Rainbow(scn, rolling=1))

  app.watch(scn)

  try:
    app.start()
  except KeyboardInterrupt:
    app.stop(forced=True)
