#!/usr/bin/env/python3

import async_messenger
from flask import Flask, request
from flask import redirect, make_response
from functools import wraps
from redis_wait import redis_wait
from spotify_const import *
from uuid import uuid4
import os
import redis
import urllib


app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        room_settings_cookie = request.cookies.get("ROOM_SETTINGS")
        service_cookie = request.cookies.get("SERVICE")
        job_id = str(uuid4())
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
            return redirect("/spotify-login", code=302)

        return redirect("/service-select", code=302)

    return decorated_function


@app.route("/")
@login_required
def index():
    return "you are logged in. this is where the preferences pages will be."


@app.route("/service-select")
def select_service():
    return '<a href="/spotify-login">Authenticate with SPOTIFY</a>'


@app.route("/spotify-login")
def spotify_login():

    state_key = str(uuid4())
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


@app.route("/spotify")
def spotify():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")
    if code is not None and r.get(state):
        room_settings_cookie = str(uuid4())
        async_messenger.send(
            "authorizer.create_authorization",
            {"code": code, "key": room_settings_cookie, "service": "spotify"},
        )

        if not redis_wait(r, room_settings_cookie):
            raise TimeoutError("0Z9MI")

        async_messenger.send(
            "user.find_or_create_user", {"room_settings_cookie": room_settings_cookie},
        )

        response = make_response(redirect("/"))
        response.set_cookie("ROOM_SETTINGS", room_settings_cookie)
        response.set_cookie("SERVICE", "spotify")
        return response
    return f"{error}: you are not logged in"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
