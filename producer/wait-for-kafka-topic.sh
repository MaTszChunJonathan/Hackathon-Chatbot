#!/usr/bin/env bash
# wait-for-kafka-topic.sh

set -e

KAFKA_HOST="$1"
KAFKA_PORT="$2"
TOPIC_NAME="$3"
shift 3
CMD="$@"

# Function to check if the topic exists
topic_exists() {
    /opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --bootstrap-server "$KAFKA_HOST:$KAFKA_PORT" --topic "$TOPIC_NAME" --describe &>/dev/null
}

# Wait for the Kafka topic to be available
until topic_exists; do
  >&2 echo "Waiting for topic '$TOPIC_NAME' to be created in Kafka..."
  sleep 5
done

>&2 echo "Topic '$TOPIC_NAME' is created - executing command"
exec $CMD