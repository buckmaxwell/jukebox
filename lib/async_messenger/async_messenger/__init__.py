#!/usr/bin/env/python3

import pika
import json


def send(queue, message, host="rabbitmq", port=5672):
    parameters = pika.ConnectionParameters(
        host=host, port=port, retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=json.dumps(message))
    connection.close()


__version__ = "0.0.1"
