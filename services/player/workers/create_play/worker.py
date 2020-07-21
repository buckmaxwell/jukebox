#!/usr/bin/env/python3

from jukebox_db import Play, Session
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
import uuid

sentry_sdk.init(
    "https://877d23fec9764314b6f0f15533ce1574@o398013.ingest.sentry.io/5253121"
)

current_module = sys.modules[__name__]

session = Session()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


QUEUE = "player.create_play"
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]


def create_play_helper(
    guid, iscr, upc, ean, spotify_id, room_code, key, key_expires_in
):

    play = Play(
        id=guid,
        isrc=iscr,
        upc=upc,
        ean=ean,
        spotify_id=spotify_id,
        room_code=room_code,
    )

    session.add(play)
    session.commit()
    r.set(key, str(play.id), ex=key_expires_in)

    return play.id


def create_play(ch, method, properties, body):

    request = json.loads(body.decode())

    guid = request["guid"]
    isrc = request["isrc"]
    upc = request["upc"]
    ean = request["ean"]
    spotify_id = request["spotify_id"]
    room_code = request["room_code"]
    key = request["key"]
    expires_in = request["expires_in"]

    create_play_helper(guid, isrc, upc, ean, spotify_id, room_code, key, expires_in)

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

            channel.basic_consume(QUEUE, create_play, auto_ack=False)
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
