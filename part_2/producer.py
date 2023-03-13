from model import Contacts, create_contact

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='direct_notification',
                         exchange_type='direct')


def main():
    contacts = Contacts.objects()
    for contact in contacts:
        severity = str(contact.favorite)
        message = str(contact.id)
        # print(severity, message)
        channel.basic_publish(exchange='direct_notification',
                              routing_key=severity,
                              body=message)
    connection.close()


if __name__ == '__main__':
    if not Contacts.objects():
        for _ in range(50):
            create_contact()

    main()
