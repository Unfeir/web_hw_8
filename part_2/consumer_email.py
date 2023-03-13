from model import Contacts

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='direct_notification', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='direct_notification', queue=queue_name, routing_key="email")


def send_notification(id):
    contact = Contacts.objects(pk=id)
    for i in contact:
        i.send_check = True
        i.save()
    print(f"notification was sending to {i.fullname}")


def callback(ch, method, properties, body):
    send_notification(body.decode())
    # print(f"{body=}\n{method.routing_key=}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()