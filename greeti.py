
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.invoking import Invoking
from luten.acts.greet import Greet # Note: These one-shot acts don't do so great on emulation (they close very quickly).

theater = Invoking()

theater.perform(Greet())

theater.start()
