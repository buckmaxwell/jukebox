#!/usr/bin/env/python3

from flask import Flask, request, jsonify
from flask import redirect, make_response
from functools import wraps
import async_messenger
import redis
import sys
import uuid


current_module = sys.modules[__name__]

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def spotify_play_song(request, authorization_id):
    uri = request.get_json()["uri"]
    job_id1, job_id2 = str(uuid.uuid4()), str(uuid.uuid4())
    async_messenger.send(
        "authorizer.make_authorized_request",
        {
            "http_verb": "post",
            "url": f"https://api.spotify.com/v1/me/player/queue?uri={uri}",
            "authorization_id": authorization_id,
            "key": job_id1,
            "expires_in": 60 * 60,
        },
    )
    async_messenger.send(
        "authorizer.make_authorized_request",
        {
            "http_verb": "put",
            "url": "https://api.spotify.com/v1/me/player/play",
            "authorization_id": authorization_id,
            "key": job_id2,
            "expires_in": 60 * 60,
        },
    )


@app.route("/", methods=["POST"])
def play_song():
    room_code = request.get_json()[
        "room_code"
    ].upper()  # could technically be a room settings cookie too
    service = request.get_json()["service"]
    if not service:
        return jsonify({"error": "bad request"}), 400
    authorization_id = r.get(room_code)
    if not authorization_id:
        return jsonify({"error": "room not found"}), 404
    getattr(current_module, f"{service}_play_song")(request, authorization_id)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
