#!/usr/bin/env/python3

from flask import Flask, request, jsonify
from flask import redirect, make_response
from flask_cors import CORS
from functools import wraps
import json
import os
import redis
import spotify_request
import sys
import urllib


current_module = sys.modules[__name__]

app = Flask(__name__)
CORS(app)

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def spotify_search_response_to_universal_format(resp_dict):
    results = []
    for track_dict in resp_dict["tracks"]["items"]:
        result_dict = {}
        result_dict["name"] = track_dict["name"]
        result_dict["service"] = "spotify"
        result_dict["type"] = track_dict["type"]
        result_dict["uri"] = track_dict["uri"]
        result_dict["id"] = track_dict["id"]
        result_dict["album_art"] = track_dict["album"]["images"][0]["url"]
        result_dict["artists"] = [a["name"] for a in track_dict["artists"]]
        results.append(result_dict)
    return results


def spotify_search(request):
    q = request.args["q"]
    types = "track"
    cached = r.get(f"spotify_{q}_{types}")
    if cached:
        return jsonify(json.loads(cached))
    resp = spotify_request.get(
        "https://api.spotify.com/v1/search", params={"q": q, "type": types},
    )

    resp.raise_for_status()

    formatted_dict = spotify_search_response_to_universal_format(resp.json())
    r.set(f"spotify_{q}_{types}", json.dumps(formatted_dict), ex=60 * 60 * 24 * 7)
    return jsonify(formatted_dict)


@app.route("/", methods=["GET"])
def search():
    return getattr(current_module, f"{request.args['service']}_search")(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
