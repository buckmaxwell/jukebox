#!/usr/bin/env/python3
import pika
import json
import redis


def send(service, method, message):
    parameters = pika.ConnectionParameters(
        host="rabbitmq", retry_delay=0.25, connection_attempts=60
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    qname = f"{service}.{method}"
    channel.queue_declare(queue=qname)
    channel.basic_publish(exchange="", routing_key=qname, body=json.dumps(message))
    connection.close()
