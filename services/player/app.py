#!/usr/bin/env/python3

import logging
import sys
import uuid
from functools import wraps

import async_messenger
import redis
import sentry_sdk
from flask import Flask, jsonify, make_response, redirect, request
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn="https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121",
    integrations=[FlaskIntegration(), RedisIntegration()],
)

current_module = sys.modules[__name__]
app = Flask(__name__)
CORS(app)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


class PlayerError(Exception):
    pass


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


@app.route("/player/", methods=["POST"])
def play_song():
    try:
        if not request.get_json():
            raise PlayerError("request must be json")
        room_code = request.get_json()["room_code"].upper()

        user_ids = []  # owner and follower users
        for i in range(r.llen(room_code)):
            user_id = r.lindex(room_code, i)
            user_ids.append(user_id)

        authorization_ids = [r.get(user_id) for user_id in user_ids if r.get(user_id)]

        if not authorization_ids:
            return jsonify({"error": "room not found or no room subscribers"}), 404

        for authorization_id in authorization_ids:
            service = r.get(authorization_id)
            if service:
                getattr(current_module, f"{service}_play_song")(
                    request, authorization_id
                )
            else:
                logging.warning(
                    f"Service unknown for authorization id {authorization_id}"
                )
        return "", 204

    except (KeyError, AttributeError, PlayerError) as e:
        return jsonify({"error": f"{e.__class__.__name__}:{e}"}), 400


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5002, debug=True)
