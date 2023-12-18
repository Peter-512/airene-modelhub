import os

import dotenv
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

dotenv.load_dotenv()

CONNECTION_STR = os.environ["MODELHUB_NAMESPACE_CONNECTION_STR"]
ENTRY_QUEUE_NAME = os.environ["MODELHUB_ENTRY_QUEUE_NAME"]
OUTPUT_QUEUE_NAME = os.environ["MODELHUB_OUTPUT_QUEUE_NAME"]


class BusServiceAccessPoint:
    """
    Access point to the bus service
    """

    def __init__(self):
        pass

    async def receive_messages(self, n=999999999):
        """
        While there are messages on the queue, receive them and add to the list.
        :param n: maximum number of messages to receive

        :return: list of messages
        """
        aggregated_messages = []
        max_messages = n
        async with ServiceBusClient.from_connection_string(
            conn_str=CONNECTION_STR,
        ) as client:
            async with client:
                has_received = True
                receiver = client.get_queue_receiver(queue_name=ENTRY_QUEUE_NAME)
                async with receiver:
                    while has_received and len(aggregated_messages) < max_messages:
                        received_msgs = await receiver.receive_messages(
                            max_message_count=1,
                            max_wait_time=5,
                        )
                        if len(received_msgs) == 0:
                            has_received = False
                        for msg in received_msgs:
                            aggregated_messages.append(str(msg))
                            await receiver.complete_message(msg)
        return aggregated_messages

    async def send_messages(self, messages):
        """
        Send a message to the queue
        """
        async with ServiceBusClient.from_connection_string(
            conn_str=CONNECTION_STR,
        ) as client:
            async with client:
                sender = client.get_queue_sender(queue_name=OUTPUT_QUEUE_NAME)
                async with sender:
                    for message in messages:
                        message = ServiceBusMessage(
                            str(message),
                            content_type="application/json",
                        )
                        await sender.send_messages(message)
