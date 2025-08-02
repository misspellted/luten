
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.invoking import Invoking

theater = Invoking()

from luten.acts.shop import Shop
from conversations import shop_walk_in

theater.perform(Shop(shop_walk_in))

theater.start()
