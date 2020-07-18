#!/usr/bin/env/python3

import os
import random
import string
import urllib
import uuid
from functools import wraps
from time import sleep

import arrow
import async_messenger
import redis
import sentry_sdk
from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from redis_wait import redis_wait

sentry_sdk.init(
    dsn="https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121",
    integrations=[FlaskIntegration(), RedisIntegration()],
)


LOGIN_LENGTH = 60 * 60 * 24 * 7  # one week
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


def create_spotify_authorization(code):
    key = str(uuid.uuid4())
    async_messenger.send(
        "authorizer.create_authorization",
        {"code": code, "key": key, "service": "spotify"},
    )
    authorization_id = redis_wait(r, key)
    if not authorization_id:
        raise TimeoutError("0Z9MI")
    return authorization_id


def find_or_create_spotify_user(authorization_id):
    key = str(uuid.uuid4())
    async_messenger.send(
        "authorizer.make_authorized_request",
        {
            "http_verb": "get",
            "url": "https://api.spotify.com/v1/me",
            "authorization_id": authorization_id,
            "queue": "user.create_or_update_user",
            "kwargs": {"ebc_host_user": key},
        },
    )
    user_id = redis_wait(r, key)
    if not user_id:
        raise TimeoutError("L9RBU")
    return user_id


@app.route("/spotify/login")
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


@app.route("/spotify/callback")
def spotify():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")
    if code is not None and r.get(state):

        # Syncronously create a spotify authorization
        auth_id = create_spotify_authorization(code)

        # Syncronously create or update a spotify authorization
        user_id = find_or_create_spotify_user(auth_id)

        # User id returns current auth in redis
        r.set(user_id, auth_id)
        r.set(auth_id, "spotify")

        # Store user and auth id in redis
        ext_auth, ext_user = str(uuid.uuid4()), str(uuid.uuid4())
        r.set(ext_auth, auth_id, ex=LOGIN_LENGTH)
        r.set(ext_user, user_id, ex=LOGIN_LENGTH)

        # Create response, setting cookies
        response = make_response(redirect("/rooms"))
        response.set_cookie("EBC_HOST_USER", ext_user, max_age=LOGIN_LENGTH)
        response.set_cookie("EBC_HOST_AUTH", ext_auth, max_age=LOGIN_LENGTH)
        response.set_cookie("EBC_HOST_SERVICE", "spotify", max_age=LOGIN_LENGTH)
        return response
    return jsonify({"error": f"{error}: you are not logged in"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)

