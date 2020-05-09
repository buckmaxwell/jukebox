#!/usr/bin/env/python3

from flask import Flask, request, jsonify
from flask import redirect, make_response
from functools import wraps
import json
import os
import redis
import spotify_request
import sys
import urllib


current_module = sys.modules[__name__]

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def spotify_search(request):
    q = request.args["q"]
    types = "track"
    cached = r.get(f"spotify_{q}_{types}")
    if cached:
        return jsonify(json.loads(cached))
    resp = spotify_request.get(
        "https://api.spotify.com/v1/search", params={"q": q, "type": types},
    )
    r.set(f"spotify_{q}_{types}", json.dumps(resp.json()), ex=60 * 60 * 24 * 7)
    return jsonify(resp.json())


@app.route("/", methods=["GET"])
def search():
    return getattr(current_module, f"{request.args.get('service')}_search")(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
