# %%
from lczero.backends import Weights, Backend, GameState
import numpy as np

w = Weights("nets/t1-512x15x8h-distilled-swa-3395000.pb.gz")

# print(w.filters())
Backend.available_backends()
b = Backend(weights=w)
# %%
g = GameState(moves=['e2e4', 'e7e5', 'g1f3', 'b8c6'])
g
# %%
print(g.as_string())
# %%
i1 = g.as_input(b)

bin(i1.mask(0))
o1 = b.evaluate(i1)[0]
print(o1.q(), o1.d(), o1.m())
p = list(o1.p_raw(*g.policy_indices()))
print(np.argmax(p), np.max(p), len(p))

