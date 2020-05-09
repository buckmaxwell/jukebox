#!/usr/bin/env/python3

from flask import Flask, request, jsonify
from flask import redirect, make_response
from functools import wraps
import json
import os
import redis
import requests
import sys
import urllib

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

current_module = sys.modules[__name__]


def spotify_refresh_non_user_access_token(request):
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials",},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    token, expires = resp.json()["access_token"], resp.json()["expires_in"]
    r.set("SPOTIFY_NON_USER_ACCESS_TOKEN", token, ex=expires)


# TODO: this process of fetching the token if there is not one could be in a
# separate service worker maybe under authorizer
def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        service = request.args["service"]
        if r.get("{service}_NON_USER_ACCESS_TOKEN".upper()) is None:
            getattr(current_module, f"{service}_refresh_non_user_access_token",)(
                request
            )
        return f(*args, **kwargs)

    return decorated_function


def spotify_search(request):
    q = request.args["q"]
    types = "track"
    cached = r.get("spotify_{q}_{types}")
    if cached:
        return jsonify(json.loads(cached))
    access_token = r.get("SPOTIFY_NON_USER_ACCESS_TOKEN")
    resp = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": q, "type": types},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    return jsonify(resp.json())


@app.route("/", methods=["GET"])
@authorization_required
def search():
    return getattr(current_module, f"{request.args.get('service')}_search")(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
