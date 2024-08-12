import os

from quixstreams import Application

from schema import Ping, Pong


DEBUG = bool(int(os.environ.get("DEBUG", 0)))
KAFKA_URL = os.environ.get("KAFKA_URL")
CONSUMER_GROUP = os.environ.get("CONSUMER_GROUP")


app = Application(
    broker_address=KAFKA_URL,  # Kafka broker address
    consumer_group=CONSUMER_GROUP,  # Kafka consumer group
    auto_offset_reset="latest",  # Read topic from the end
    producer_extra_config={
        "enable.idempotence": True,
    },
    loglevel="DEBUG" if DEBUG else "INFO",
    processing_guarantee="at-least-once",  # exactly once semantic needs more than 1 broker running (most likely 3 at minimum)
)

ping_topic = app.topic("ping", value_deserializer="json")
pong_topic = app.topic("pong", value_serializer="json")


def pong(value):
    return Pong(message="pong", timestamp=value["timestamp"])


def main():
    ping_consumer = (
        app.dataframe(ping_topic)
        .print(pretty=True, metadata=True)
        .update(pong)
        .drop("message_to_delete")
        .to_topic(pong_topic)
    )
    app.run(ping_consumer)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt")
