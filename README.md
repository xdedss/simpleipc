
# SimpleIPC

```
requirements:
python-socketio
gevents
```

A simple python script that allows you to call a function running another process (script2.py), as shown in script1.py

1. run script1.py, which starts a server, hosting the function `pow2`
2. run script2.py, which connects to the server and call the `pow2` with some numbers, and gets return values

Note that for simplicity, the function you host must have exactly one argmnent of type `bytes` and one return value of type `bytes`. However, with pickle.dumps and pickle.loads, you can easily wrap it to process multiple argmnents of any types.

