#!/usr/bin/env/python3

from db import User, Session
import json
import pika
import sys

current_module = sys.modules[__name__]

session = Session()


QUEUE = "user.create_or_update_user"

def spotify_email_fetcher(profile):
    return profile["body"]["email"]


def create_or_update_user_helper(profile, service):

    email = getattr(current_module, f"{service}_email_fetcher")(profile)

    try:
        user = session.query(User).filter(User.email == email).filter(User.service == service).one()
    except:
        user = User(
            email=email,
            service=service,
            profile=profile
        )

    session.add(user)
    session.commit()


def create_or_update_user(ch, method, properties, body):

    request = json.loads(body.decode())
    profile = request["body"]
    service = request["service"]

    create_or_update_user_helper(profile, service)

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
