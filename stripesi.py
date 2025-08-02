
import logging, time
logging.basicConfig(filename=f"logs/luten-{time.time_ns()}.log", filemode="w", level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

from luten.theaters.invoking import Invoking
from luten.acts.stripes import Stripes # The VS Code integrated terminal (using Bash) on Arch Linux doesn't like this Act. Very much warn for flashing lights.

# TODO: Investigate maybe using threads to move print-to-buffer updates outside of terminal-refresh updates. Or... whatever better wording would be used in this comment.

theater = Invoking()

theater.perform(Stripes(250, 1)) # Limit to 250 updates; don't want it acting forever!

theater.start()
