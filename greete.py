
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.piegame import Emulated
from luten.acts.greet import Greet # Note: These one-shot acts don't do so great on emulation (they close very quickly).

theater = Emulated(80, 25)

theater.perform(Greet())

theater.start()
