# /bin/bash

# Create the sentiment_analysis_twiter topic
docker exec -it kafka opt/kafka/bin/kafka-topics.sh \
    --create --zookeeper zookeeper:2181 \
    --topic sentiment-analysis-twiter \
    --partitions 1 \
    --replication-factor 1

# Topic details
docker exec -it kafka opt/kafka/bin/kafka-topics.sh \
    --describe --zookeeper zookeeper:2181