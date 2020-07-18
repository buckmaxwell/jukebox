#!/usr/bin/env/python3

import os
import random
import string
import urllib
import uuid
from functools import wraps

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

from db import Room, Session
from redis_wait import redis_wait

sentry_sdk.init(
    dsn="https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121",
    integrations=[FlaskIntegration(), RedisIntegration()],
)

ROOM_LIFESPAN = 60 * 60 * 24  # one day

app = Flask(__name__)
CORS(app)

session = Session()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def random_room_code():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for i in range(4)
    )


def add_room(user_id):
    room_code = random_room_code()

    room = Room(
        code=room_code,
        host=user_id,
        expiration=arrow.now().shift(seconds=ROOM_LIFESPAN).datetime,
    )
    session.add(room)
    session.commit()

    r.rpush(room_code, str(user_id))
    r.expire(room_code, ROOM_LIFESPAN)
    return room_code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ebc_host_auth = request.cookies.get("EBC_HOST_AUTH")
        service = request.cookies.get("EBC_HOST_SERVICE")
        job_id = str(uuid.uuid4())

        authorization_id = r.get(ebc_host_auth) if ebc_host_auth else None
        if authorization_id:
            async_messenger.send(
                "authorizer.refresh_authorization",
                {
                    "authorization_id": authorization_id,
                    "job_id": job_id,
                    "service": service,
                },
            )
            if redis_wait(r, job_id):
                return f(*args, **kwargs)

        response = make_response(redirect("/rooms"))
        response.set_cookie("EBC_HOST_AUTH", "", expires=0)
        response.set_cookie("EBC_HOST_USER", "", expires=0)
        response.set_cookie("EBC_HOST_SERVICE", "", expires=0)
        return response

    return decorated_function


@app.route("/host/rooms", methods=["GET", "POST"])
@login_required
def my_rooms():
    user_id = r.get(request.cookies["EBC_HOST_USER"])

    if request.method == "POST":
        room_code = add_room(user_id)
        return room_code, 201

    # TODO: add followers - join table between rooms and users
    rooms = session.query(Room).filter(Room.host == user_id).all()
    data = []
    for room in rooms:
        # TODO: this is not an ideal serialization strategy
        data.append(
            {
                "id": str(room.id),
                "code": room.code,
                "expiration": room.expiration,
                "expiration_human": arrow.get(room.expiration).humanize(),
                "role": "host" if str(room.host) == user_id else "follower",
            }
        )

    return jsonify(data)


@app.route("/host/room/<room_code>", methods=["GET"])
def public_room(room_code):
    # TODO: should rooms REALLY be associated with a service. No of course not?
    # Or maybe they should because the search service used should be the search
    # service for the user? But probably best to just always use spotify to
    # search... and then use the isbn equivalent for tracks to convert between
    # services.
    if r.get(room_code.upper()):
        return jsonify({"room_code": room_code}), 200
    return jsonify({"error": "resource not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
