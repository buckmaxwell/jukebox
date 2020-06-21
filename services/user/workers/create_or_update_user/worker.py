#!/usr/bin/env/python3

from db import User, Session
import json
import pika
import sys
import redis

current_module = sys.modules[__name__]

session = Session()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


QUEUE = "user.create_or_update_user"


def spotify_email(profile):
    return profile["email"]


def spotify_service_key(profile):
    return profile["id"]


def create_or_update_user_helper(profile, service):

    email = getattr(current_module, f"{service}_email")(profile)
    service_key = getattr(current_module, f"{service}_service_key")(profile)

    try:
        user = (
            session.query(User)
            .filter(User.service_key == service_key)
            .filter(User.service == service)
            .one()
        )
    except:
        user = User(
            email=email, service=service, service_key=service_key, profile=profile,
        )

    session.add(user)
    session.commit()
    return user.id


def create_or_update_user(ch, method, properties, body):

    request = json.loads(body.decode())
    profile = request["body"]
    service = request["service"]
    ebc_host_user = request["ebc_host_user"]

    user_id = create_or_update_user_helper(profile, service)

    r.set(ebc_host_user, user_id)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(QUEUE, create_or_update_user, auto_ack=False)
    channel.start_consuming()
