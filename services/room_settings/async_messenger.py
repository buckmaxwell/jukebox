#!/usr/bin/env/python3
import pika
import json
import redis


def send(queue, message):
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=json.dumps(message))
    connection.close()
