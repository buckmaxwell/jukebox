#!/usr/bin/env/python3

from db import Authorization, Session
from time import sleep
import arrow
import json
import logging
import os
import pika
import redis
import requests
import sentry_sdk
import sys

sentry_sdk.init(
    "https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121"
)

current_module = sys.modules[__name__]

session = Session()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


QUEUE = "authorizer.create_authorization"
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]


def spotify_request_resolver(code):
    return requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,  # validation only
        },
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )


def create_authorization_helper(code, key, service):

    resp = getattr(current_module, f"{service}_request_resolver")(code)

    resp.raise_for_status()

    auth = Authorization(
        access_token=resp.json()["access_token"],
        scope=resp.json()["scope"],
        access_token_expiration=arrow.now()
        .shift(seconds=resp.json()["expires_in"])
        .datetime,
        refresh_token=resp.json()["refresh_token"],
        service=service,
    )

    session.add(auth)
    session.commit()
    r.set(key, str(auth.id), ex=resp.json()["expires_in"])

    return auth.id


def create_authorization(ch, method, properties, body):

    request = json.loads(body.decode())
    code = request["code"]
    key = request["key"]
    service = request["service"]

    create_authorization_helper(code, key, service)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=1.0, connection_attempts=60
    )
    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE)
            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(QUEUE, create_authorization, auto_ack=False)
            channel.start_consuming()
        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker as e:
            raise e
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError as e:
            raise e
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            sleep(0.25)
            continue
