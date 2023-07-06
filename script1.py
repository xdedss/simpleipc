
import numpy as np
import pickle

import simpleipc

server = simpleipc.Server(8888)

@server.listen('pow2')
def foo(arg):
    nums = pickle.loads(arg)
    res = np.power(nums, 2)
    return pickle.dumps(res)


server.run()

print(123)
