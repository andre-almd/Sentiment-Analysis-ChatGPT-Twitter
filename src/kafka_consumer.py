"""
This script performs sentiment analysis on streaming Twitter data using Apache Spark and Kafka.
"""

# Imports
import os
import time
import random

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import col

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze sentiment of a given text.

    Parameters:
    text (str): The text to analyze sentiment.

    Returns:
    str: The sentiment of the text. 'Positive', 'Negative' or 'Neutral'.
    """

    # Check if text is None or empty
    if text is None or text == '':
        return 'Neutral'

    sentiment_score = sid.polarity_scores(text)['compound']
    if sentiment_score >= 0.05:
        return 'Positive'
    elif sentiment_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


# Kafka server port
SERVER = 'localhost:9092'

# Topic name
TOPIC = 'sentiment-analysis-twiter'

# Spark Conectors for Apache Kafka
spark_jars = ("{},{},{},{},{}".format(os.getcwd() + "/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar",
                                      os.getcwd() + "/jars/kafka-clients-3.5.0.jar",
                                      os.getcwd() + "/jars/spark-streaming-kafka-0-10_2.13-3.5.0.jar",
                                      os.getcwd() + "/jars/commons-pool2-2.12.0.jar",
                                      os.getcwd() + "/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar"))

# initialize Spark session
spark = SparkSession.builder.config("spark.jars", spark_jars).appName(
    "sentiment-analysis-twiter").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Dataframe to store streaming
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", SERVER) \
    .option("subscribe", TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

streaming_df = df.selectExpr("CAST(value AS STRING)", "timestamp")

# Data schema
def_schema = 'tweet_timestamp STRING, content STRING'

streaming_df = streaming_df.select(
    from_csv(col("value"), def_schema).alias("tweet"), "timestamp")

# Create a view in Spark memory to see schema
streaming_df.select('tweet.content', 'timestamp')
streaming_df.createOrReplaceTempView("tweets_View")
print(streaming_df.printSchema())

# Get data from stream
tweets_stream = spark.sql("SELECT * FROM tweets_View")

tweets_stream_spark = tweets_stream.writeStream.trigger(processingTime='3 seconds') \
    .outputMode('append') \
    .format('memory') \
    .queryName("spark_table") \
    .start()

tweets_stream_spark.awaitTermination(1)

spark_tweets = spark.sql("SELECT * FROM spark_table")

print('Streaming tweets...')
while True:
    tweets_data = spark_tweets.select("tweet.tweet_timestamp", "tweet.content")
    tweets_data = tweets_data.orderBy("tweet.tweet_timestamp", ascending=False)

    total_count = tweets_data.count()
    print(f'Tweets in stream: {total_count}')

    # Apply sentiment analysis to each tweet
    analyze_sentiment_udf = udf(analyze_sentiment, StringType())
    tweets_data = tweets_data.withColumn(
        "sentiment", analyze_sentiment_udf("content"))

    # Count the classes of sentiment
    sentiment_counts = tweets_data.groupBy("sentiment").count().orderBy(
        "count", ascending=False)

    # Calculate the percentage for each sentiment class
    sentiment_counts = sentiment_counts.withColumn(
        "percentage (%)", col("count") / total_count * 100)

    tweets_data.show(5, truncate=100)

    print("Sentiment Counts:")
    sentiment_counts.show()

    time.sleep(1)
