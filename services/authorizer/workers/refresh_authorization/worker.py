#!/usr/bin/env/python3

from db import Authorization, Session
import arrow
import json
import os
import pika
import redis
import requests
import sys

current_module = sys.modules[__name__]

session = Session()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


QUEUE = "authorizer.refresh_authorization"
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def spotify_request_resolver(refresh_token):
    return requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )


def refresh_authorization_helper(authorization_id, job_id, service):
    authorization = session.query(Authorization).get(authorization_id)
    resp = getattr(current_module, f"{service}_request_resolver")(
        authorization.refresh_token
    )

    resp.raise_for_status()

    access_token = resp.json()["access_token"]
    expires = arrow.now().shift(seconds=resp.json()["expires_in"]).datetime

    authorization.access_token = access_token
    authorization.access_token_expiration = expires

    session.commit()
    r.set(job_id, "1", ex=60 * 60)


def refresh_authorization(ch, method, properties, body):
    request = json.loads(body.decode())
    authorization_id = request["authorization_id"]
    job_id = request["job_id"]
    service = request["service"]

    refresh_authorization_helper(authorization_id, job_id, service)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(QUEUE, refresh_authorization, auto_ack=False)
    channel.start_consuming()
