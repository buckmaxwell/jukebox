#!/usr/bin/env/python3


def room(room, user_id):
    {
        "id": room.id,
        "code": room.code,
        "expiration": room.expiration,
        "role": "host" if room.host == user_id else "follower",
    }


__version__ = "0.0.1"
