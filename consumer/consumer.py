from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer('test-topic', bootstrap_servers='kafka-1:9092', api_version=(0,10,2))
#value_deserializer=lambda v: json.loads(v.decode('utf-8')),

client = MongoClient('mongodb://mongodb:27017/')

db = client['kafka_db']
collection = db['kafka_collection']
print("Connected to MongoDB")

#test_data = {"test1":"hello"}
#collection.insert_one(test_data)

#try:
#    for message in consumer:
#        collection.insert_many(message)
#        print(f"Inserted: {message}")
#except:
#    print("fail to insert")

# Assuming you've already set up your Kafka consumer and connected to MongoDB
# consumer = ... (Your Kafka consumer setup)
# collection = ... (Your MongoDB collection setup)

try:
    for message in consumer:
        # Deserialize the message from Kafka
        message_value = message.value.decode('utf-8')
        data = json.loads(message_value)
#        print(data)
        # Ensure 'data' is a list of dictionaries
        if isinstance(data, list) and all(isinstance(d, dict) for d in data):
            # Insert the list of dictionaries into MongoDB
            collection.insert_many(data)
            print(f"Inserted")
        else:
            print(f"Unexpected message format:")

except Exception as e:
    print(f"Failed to insert: {e}")
