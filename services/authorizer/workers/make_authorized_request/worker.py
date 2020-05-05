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


QUEUE = "authorizer.make_authorized_request"
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def spotify_request_resolver(http_verb, url, access_token):
    return getattr(requests, http_verb.lower())(
        url, headers={"Authorization": "Bearer {}".format(access_token)}
    )


def make_authorized_request_helper(http_verb, url, authorization_id):
    authorization = session.query(Authorization).get(authorization_id)
    return getattr(current_module, f"{authorization.service}_request_resolver")(
        http_verb, url, authorization.access_token
    )


def record_key_response_helper(resp_dict, key, expires_in):
    r.set(key, json.dumps(resp_dict), ex=expires_in)


def record_queue_response_helper(resp_dict, queue):
    async_messenger.send(queue, resp_dict)


def response_to_dict(resp):
    return {
        "body": resp.json(),
        "status_code": resp.status_code,
        "headers": resp.headers,
        "url": resp.url,
    }


def make_authorized_request(ch, method, properties, body):
    request = json.loads(body.decode())
    http_verb = request["http_verb"]
    url = request["url"]
    authorization_id = request["authorization_id"]

    queue = request.get("queue")
    key, expires_in = None, None
    if queue is None:
        key = request["key"]
        expires_in = request["expires_in"]

    resp = make_authorized_request_helper(http_verb, url, authorization_id)
    resp_dict = response_to_dict(resp)

    record_queue_response_helper(
        resp_dict, queue
    ) if queue else record_key_response_helper(resp_dict, key, expires_in)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(QUEUE, make_authorized_request, auto_ack=False)
    channel.start_consuming()
