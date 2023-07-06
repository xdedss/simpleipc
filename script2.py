
import numpy as np
import pickle
import simpleipc

# client = simpleipc.Client('127.0.0.1', 8888)
with simpleipc.Client('127.0.0.1', 8888) as client:

    xs = np.array((1,2,3,4,5))
    res = client.call('pow2', pickle.dumps(xs))
    ys = pickle.loads(res)
    print(ys)