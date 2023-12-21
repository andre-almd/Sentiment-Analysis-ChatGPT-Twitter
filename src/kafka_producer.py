"""XXXXXXXXXXXXXXXXXX"""

import time
import pandas as pd
import kafka
from kafka import KafkaProducer

print('Reading data with tweets related to ChatGPT from Jan/2023 to Mar/2023')

df = pd.read_csv('data/twitter_Jan_Mar.csv', delimiter=',')
df = df.dropna()

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')
df = df.reset_index(drop=True)
df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

print(f'Dataset lenght: {df.shape}')

# Kafka server port
SERVER = 'localhost:9092'

# Topic name
TOPIC = 'sentiment-analysis-twiter'

# Create Producer
producer = KafkaProducer(bootstrap_servers=SERVER,
                         value_serializer=None,
                         acks='all')

#print(f'Connected to Kafka. Broker Metadata: {producer.metrics()}')


for _, tweet in df.iterrows():
    sending = []

    sending.append(tweet['date'])
    sending.append(tweet['content'])

    tweet_data = ','.join(str(x) for x in sending)

    try:
        producer.send(topic=TOPIC, value=tweet_data.encode('utf-8'))
        producer.flush()
        print(f'Enviando tweet: {tweet_data}')
    except kafka.errors.ProducerFenced as e:
        print(f"Producer got fenced: {e}")
    except kafka.errors.KafkaTimeoutError as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Error sending message: {e}")

    time.sleep(1)
