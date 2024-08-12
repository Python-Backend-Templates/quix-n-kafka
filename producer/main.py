import time
import json
import os

from quixstreams import Application


DEBUG = bool(int(os.environ.get("DEBUG", 0)))
KAFKA_URL = os.environ.get("KAFKA_URL")
PRODUCER_GROUP = os.environ.get("PRODUCER_GROUP")


# connect to your local Kafka broker
app = Application(
    broker_address=KAFKA_URL,
    consumer_group=PRODUCER_GROUP,
    auto_offset_reset="latest",  # Read topic from the end
    producer_extra_config={
        "enable.idempotence": True,
    },
    loglevel="DEBUG" if DEBUG else "INFO",
    processing_guarantee="at-least-once",  # exactly once semantic needs more than 1 broker running (most likely 3 at minimum)
)

ping_topic = app.topic("ping", value_deserializer="json")
pong_topic = app.topic("pong", value_serializer="json")


def get_ping():
    return {
        "message": "ping",
        "message_to_delete": "message_to_delete",
        "timestamp": int(time.time_ns()),
    }


def main():
    with app.get_producer() as producer, app.get_consumer() as consumer:
        consumer.subscribe(topics=["pong"])
        while True:
            time.sleep(5)
            # Producer
            message = get_ping()
            producer.produce(
                topic=ping_topic.name, key="key", value=json.dumps(message)
            )

            # Consumer
            msg = consumer.poll(0.001)
            if msg is None:
                continue
            if msg.error():
                print("Kafka error:", msg.error())
                continue
            value = msg.value()
            print(value, "----------------------------------", sep="\n")
            # Store the offset of the processed message on the Consumer
            # for the auto-commit mechanism.
            # It will send it to Kafka in the background.
            # Storing offset only after the message is processed enables at-least-once delivery
            # guarantees.
            consumer.store_offsets(message=msg)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt")
