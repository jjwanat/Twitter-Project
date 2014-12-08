import redis
import gevent
import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask, render_template
from flask_sockets import Sockets

app = Flask(__name__)
redis = redis.Redis('localhost')
sockets = Sockets(app)

class Updater(object):
    def __init__(self, redis):
        self.clients = []
        self.redis = redis
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe("hashtag")

    def send(self, client, data):
        try:
            client.send(str(data['data']))
        except:
            self.clients.remove(client)

    def run(self):
        for data in (data for data in self.pubsub.listen()):
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

updater = Updater(redis)

updater.start()

@socket.route('/hashtag')
def hashtag(ws):
    updater.clients.append(ws)
    while True: gevent.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
