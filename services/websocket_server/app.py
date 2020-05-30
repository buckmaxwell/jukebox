import eventlet

eventlet.monkey_patch()

from flask import Flask, render_template

from flask_socketio import SocketIO, join_room, leave_room, send, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["WSS_SECRET"]
socketio = SocketIO(app, message_queue="redis://redis:6379/")


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


@socketio.on("message")
def handle_message(message):
    print("received message: " + message)


@socketio.on("json")
def handle_json(json):
    print("received json: " + str(json))


@socketio.on("song queued")
def handle_my_custom_event(json):
    print("received json: " + str(json))


if __name__ == "__main__":
    socketio.run(app)
