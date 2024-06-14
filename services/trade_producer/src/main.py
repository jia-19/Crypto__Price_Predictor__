# Create an Application instance with Kafka configs
from quixstreams import Application
from typing import List, Dict

from src.kraken_api import KrakenWebsocketAPI

def produce_trades(
        kafka_broker_address: str,
        kafka_topic_name:str
) -> None:
    """
        Reads trades from Kraken API and sends them through
        our Kafka topic

        Args:
            kafka_broker_address (str): Address of Kafka topic
            kafka_topic_name (str): The name of the Kafka topic

        Returns:
            None
    """
    app = Application(kafka_broker_address)

    # Defined topic -> trade with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

     # Creat API instance
    kraken_api = KrakenWebsocketAPI(product_id="BTC/USD")
    

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:

            # Fetching trades from API
            trades: List[Dict] = kraken_api.get_trades()

            for trade in trades:

                # Serialize an event using the defined Topic 
                message = topic.serialize(key=trade["product_id"], 
                                          value=trade)

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name, 
                    value=message.value, 
                    key=message.key
                )

                print("Message Sent!")
            from time import sleep
            sleep(1)

if __name__ == "__main__":
    produce_trades(kafka_broker_address= 'localhost:19092',
                kafka_topic_name= "trade" )