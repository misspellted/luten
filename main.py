
from luten.application import PyGameTerm

deltas = list()

app = PyGameTerm()
# app.on_delta = lambda delta_nanos: deltas.append(delta_nanos)

# For testing, the traditional is only fair.
motd = bytes("Hello, World!", "UTF-8")
for i in range(len(motd)):
  app.set_char(motd[i])
  app.advance()

# def rainbow(delta_nanos:int):
#   deltas.append(delta_nanos)
#   app.hidden = True
#   for row in range(app.rows):
#     for column in range(app.columns):
#       app.set_back((row * app.columns + column) & 0xF)
#       app.advance()

#     # Rolling rainbow.
#     app.advance()

# app.on_delta = rainbow

try:
  app.start()
except Exception as e:
  print(e)
  app.stop(forced=True)

if 0 < len(deltas):
  avg_delta_ns = sum(deltas)/len(deltas)
  print(f"Average delta time (ns): {avg_delta_ns}")
  print(f"Average delta time (ms): {avg_delta_ns/1e6}")
