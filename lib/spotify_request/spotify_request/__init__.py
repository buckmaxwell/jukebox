#!/usr/bin/env/python3

import json
import redis
import requests
import logging
import os


r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def refresh_non_user_access_token():
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials",},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )

    resp.raise_for_status()

    token, expires = resp.json()["access_token"], resp.json()["expires_in"]
    r.set("SPOTIFY_NON_USER_ACCESS_TOKEN", token, ex=expires)


def get(url, **kwargs):
    if not r.get("SPOTIFY_NON_USER_ACCESS_TOKEN"):
        refresh_non_user_access_token()
    kwargs["headers"] = {
        "Authorization": "Bearer {}".format(r.get("SPOTIFY_NON_USER_ACCESS_TOKEN"))
    }
    return requests.get(url, **kwargs)


__version__ = "0.0.1"
