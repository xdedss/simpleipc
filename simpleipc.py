

import socketio
# import eventlet
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import pickle, time

class Client:
    def __init__(self, host, port):
        self.sio = socketio.Client()
        self.sio.connect(f'http://{host}:{port}')
        self.result = None
        self.result_ok = False

        @self.sio.event
        def connect():
            print(f'Connected to server: {host}:{port}')

        @self.sio.on('result')
        def handle_result(result):
            # print('result!')
            self.result = result
            self.result_ok = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def call(self, func_name, arg):
        self.sio.emit(func_name, arg)
        while (not self.result_ok):
            time.sleep(0.001)
        self.result_ok = False
        return self.result

    def close(self):
        self.sio.disconnect()

class Server:
    def __init__(self, port):
        self.sio = socketio.Server(async_mode='gevent')
        self.app = socketio.WSGIApp(self.sio)
        self.port = port

        @self.sio.event
        def connect(sid, environ):
            print(f'Connected to client: {sid}')

    def listen(self, event_name):
        def decorator(func):
            @self.sio.on(event_name)
            def wrapper(sid, arg):
                try:
                    result = func(arg)
                except Exception:
                    result = pickle.dumps(None)
                print('sending', result)
                self.sio.emit('result', result, to=sid)

            return wrapper

        return decorator

    def run(self):
        print('running server')
        self.server = WSGIServer(('0.0.0.0', self.port), self.app, handler_class=WebSocketHandler)
        self.server.serve_forever()
        # eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)
        # socketio.run(self.app, port=self.port)
