
from luten.application import PyGameApp
from luten.scene import PyGameTerm
from luten.act import Greeting, Rainbow

deltas = list()

app = PyGameApp()
app.on_delta = lambda delta_nanos: deltas.append(delta_nanos)

scn = PyGameTerm()

if app.open(*scn.dimensions):
  # scn.watch(Greeting(scn))
  # scn.watch(Rainbow(scn))
  scn.watch(Rainbow(scn, rolling=1))

  app.watch(scn)

  try:
    app.start()
  except KeyboardInterrupt:
    app.stop(forced=True)

if 0 < len(deltas):
  avg_delta_ns = sum(deltas)/len(deltas)
  print(f"Average delta time (ns): {avg_delta_ns}")
  print(f"Average delta time (ms): {avg_delta_ns/1e6}")
