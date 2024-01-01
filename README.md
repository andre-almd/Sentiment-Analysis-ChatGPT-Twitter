# Sentiment-Analysis-ChatGPT-Twitter
## **This is a project from the Data Scientist Training at the [Data Science Academy](https://www.datascienceacademy.com.br/)**

![](img/img.png)
Image created with Midjourney AI

ChatGPT is the AI-based conversational system offered by OpenAI. It was launched in late 2022 and has since garnered attention from the general public, who have finally realized how AI has evolved and is already among us. 

Sentiments about ChatGPT have divided opinions. While some acknowledge that ChatGPT can be a useful tool for various daily activities, others express concerns about being replaced by AI. But which sentiment prevails on social media? 

Answering this question is my task in this project. Through the analysis of tweets about ChatGPT, I should build an analysis process that allows identifying the predominant sentiment, especially on Twitter, regarding ChatGPT: Positive, Negative or Neutral.

## Project Information

The project was implemented using **Docker**, **Kafka**, and **PySpark** technologies.

As the new free version of the Twitter API no longer allows connection for data streaming, the '**500k ChatGPT-related Tweets Jan-Mar 2023**' dataset available on Kaggle was used. You can find the dataset [here](https://www.kaggle.com/datasets/khalidryder777/500k-chatgpt-tweets-jan-mar-2023). Throughout the project, I renamed the file to 'twitter_Jan_Mar.csv'.

The entire project was executed in a **Linux** environment.

## Steps for Project Execution

1. Download the dataset from Kaggle indicated in the link above, rename it to 'twitter_Jan_Mar.csv', and place it inside the data folder. Then open the terminal in the project's root folder for the next steps.

2. Create a virtual environment named venv using [virtual enviroment](https://virtualenv.pypa.io/en/latest/installation.html).

3. Activate the virtual enviroment

4. Install the libraries required:

    ```pip3 install -r requirements.txt```

5.  Make the create_kafka_topic.sh file executable with the following command:

    ```chmod +x create_kafka_topic.sh```

6. With Docker installed, run the following command in the terminal to create containers with Kafka and Zookeeper.

    ```make run```

7. After creating the containers, execute the following command in the same terminal to create the Kafka topic:

    ```./create_kafka_topic.sh```

8. After creating the topic, start the Kafka producer in the same terminal to begin sending tweet data to the topic:

    ```python3 src/kafka_producer.py```

9. Open a new terminal to execute the Kafka consumer and consume data from the Kafka topic with PySpark streaming. Execute script the inside virtual enviroment:

    ```python3 src/kafka_consumer.py```

## A brief description of the scripts:

- **create_kafka_topic.sh**:
    This Bash script is designed to automate the setup of a Kafka topic named "sentiment-analysis-twitter". It uses Docker to interact with Kafka. The script first creates the Kafka topic with a single partition and replication factor of 1. Following the creation, it retrieves and displays details about the newly created topic using the --describe option. The script assumes that the Kafka broker is running in a Docker container, and it communicates with the ZooKeeper service on the specified host and port (zookeeper:2181).

- **kafka_producer.py**:
    This Python script reads tweets related to ChatGPT from a CSV file, processes the data, and sends it to a Kafka topic. It uses the KafkaProducer to push each tweet's date and content to the specified topic. The purpose is to feed a Kafka topic with relevant tweet data for subsequent sentiment analysis.

- **kafka_consumer.py**:
    This Python script integrates Apache Spark and Kafka to conduct real-time sentiment analysis on streaming Twitter data. It defines a sentiment analysis function using NLTK's VADER analyzer, configures Spark to read and process data from Kafka, and continuously analyzes sentiments, presenting insights such as total tweet count, sentiment class distribution, and percentages.

\
![](img/video.gif)