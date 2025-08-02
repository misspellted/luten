
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.piegame import Emulated
from luten.acts.rain import Rain

theater = Emulated(80, 25)

theater.perform(Rain(250)) # Limit to 250 updates; don't want it acting forever!

theater.start()
