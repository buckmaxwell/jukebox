#!/usr/bin/env/python3

from flask import Flask, request, url_for, jsonify
from flask import redirect, make_response, render_template
from flask_cors import CORS
from functools import wraps
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from time import sleep
import async_messenger
import os
import random
import redis
import sentry_sdk
import string
import urllib
import uuid

sentry_sdk.init(
    dsn="https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121",
    integrations=[FlaskIntegration(), RedisIntegration()],
)

# Constants

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_API_SCOPES = [
    "playlist-modify-private",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-playback-state",
    "streaming",
    "app-remote-control",
    "playlist-modify-public",
    "playlist-read-collaborative",
    "playlist-read-private",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-recently-played",
    "user-top-read",
]

app = Flask(__name__)
CORS(app)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def create_spotify_authorization(external_authorization_id, code):
    async_messenger.send(
        "authorizer.create_authorization",
        {"code": code, "key": external_authorization_id, "service": "spotify"},
    )
    authorization_id = redis_wait(r, external_authorization_id)
    if not authorization_id:
        raise TimeoutError("0Z9MI")
    return authorization_id


def find_or_create_spotify_user(external_user_id, authorization_id):
    async_messenger.send(
        "authorizer.make_authorized_request",
        {
            "http_verb": "get",
            "url": "https://api.spotify.com/v1/me",
            "authorization_id": authorization_id,
            "queue": "user.find_or_create_user",
            "args": {"external_user_id": external_user_id},
        },
    )
    user_id = redis_wait(r, external_user_id)
    if not user_id:
        raise TimeoutError("L9RBU")
    return user_id


def redis_wait(
    redis, key, time=15,
):
    sleep_time = 0.25
    tries = int(time / sleep_time)
    result = None
    for _ in range(tries):
        result = redis.get(key)
        if result:
            return result
        sleep(0.25)
    return result


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        room_settings_cookie = request.cookies.get("ROOM_SETTINGS")
        service_cookie = request.cookies.get("SERVICE")
        job_id = str(uuid.uuid4())
        authorization_id = r.get(room_settings_cookie) if room_settings_cookie else None
        if authorization_id:
            async_messenger.send(
                "authorizer.refresh_authorization",
                {
                    "authorization_id": authorization_id,
                    "job_id": job_id,
                    "service": service_cookie,
                },
            )
            if redis_wait(r, job_id):
                return f(*args, **kwargs)

        if service_cookie == "spotify":
            return redirect("/host/spotify-login", code=302)

        return redirect("/host/service-select", code=302)

    return decorated_function


@app.route("/host/room/<room_code>", methods=["GET"])
def public_room(room_code):
    if r.get(room_code.upper()) and r.get(f"{room_code.upper()}_service"):
        return (
            jsonify(
                {
                    "room_code": room_code,
                    "service": r.get(f"{room_code.upper()}_service"),
                }
            ),
            200,
        )
    return jsonify({"error": "resource not found"}), 404


@app.route("/host/spotify-login")
def spotify_login():
    state_key = str(uuid.uuid4())
    r.set(state_key, "1", ex=60 * 30)
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": state_key,
        "scope": " ".join(SPOTIFY_API_SCOPES),
        "show_dialog": "false",
    }
    new_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return redirect(new_url, code=302)


@app.route("/host/spotify/callback")
def spotify():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")
    if code is not None and r.get(state):

        external_auth_id = str(uuid.uuid4())
        external_user_id = str(uuid.uuid4())
        auth_id = create_spotify_authorization(external_auth_id, code)
        _ = find_or_create_spotify_user(external_user_id, auth_id)

        response = make_response(redirect("/rooms/"))
        response.set_cookie("EBC_HOST_ID", external_user_id)
        response.set_cookie("EBC_HOST_SERVICE", "spotify")
        return response
    return jsonify({"error": f"{error}: you are not logged in"}), 400


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
