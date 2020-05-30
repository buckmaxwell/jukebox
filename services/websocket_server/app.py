from flask import Flask, render_template
from flask_cors import CORS


from flask_socketio import SocketIO, join_room, leave_room, send, emit

# from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.environ["WSS_SECRET"]
socketio = SocketIO(app)
# socketio = SocketIO(app, message_queue="redis://redis:6379/")


@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(username + " has entered the room.", room=room)


@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send(username + " has left the room.", room=room)


@app.route("/socket.io/")
def socket_home():
    return "socket home"


@app.route("/")
def index():
    return "index"


@socketio.on("message")
def handleMessage(msg):
    print("Message: " + msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5003, debug=True)
