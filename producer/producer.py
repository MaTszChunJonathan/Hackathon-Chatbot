from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaProducer
import time
import requests
from bs4 import BeautifulSoup
import json
import re
from masquer import masq
import random

KAFKA_HOST = "kafka-1"
KAFKA_PORT = "9092"
TOPIC_NAME = "test-topic"

def check_or_create_topic(topic_name):
    retries = 5
    while retries > 0:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
                client_id='test'
            )
            topic_list = []
            topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
            print("Connected to Kafka")

            try:
                admin_client.create_topics(new_topics=topic_list, validate_only=False)
                print(f"Topic '{topic_name}' created successfully.")
            except TopicAlreadyExistsError:
                print(f"Topic '{topic_name}' already exists.")
            break
        except:
            print("Kafka broker is not available. Retrying...")
            retries -= 1
            time.sleep(5)

check_or_create_topic(TOPIC_NAME)

producer = KafkaProducer(bootstrap_servers='kafka-1:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'), api_version=(0,10,2))

#data = {'test':'message'}

#producer.send('test-topic', data)

#producer.flush()

# URL to fetch
#url = 'https://zh.escapade.com.hk/search?q=cycling'

# Send a GET request to the URL
#response = requests.get(url)

# Check if the request was successful
#if response.status_code == 200:
#    # Parse the HTML content
#    soup = BeautifulSoup(response.content, 'html.parser')
#    
#    # Find the script tag with the specific ID
#    script_tag = soup.find('script', {'id': 'web-pixels-manager-setup'})
#    
#    pattern = r'\[\{\"price\":.*?\}\]'
#
    # Search for the pattern
#    matches = re.findall(pattern, str(script_tag))

#    json_data = json.loads(matches[0])

#    print(json_data)

#    with open('output.json', 'w') as json_file:
#        json.dump(json_data, json_file, indent=4)

#    producer.send('test-topic', json_data)

#    producer.flush()

#else:
#    print(f"Failed to retrieve the page. Status code: {response.status_code}")



url = "https://p7hdnsd47u-dsn.algolia.net/1/indexes/prod_pim_v1_index/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.15.0)%3B%20Browser%20(4.15.0)"

hits_ls = list()

i = 0
try:
    while i < 3: # just scrape 3
        useragent = masq(
                    ua = True,  # user-agent, defaults to True
                    rf = False,  # referer, defaults to False
                    hd = False,  # header-data, defaults to False
                )

        useragent['x-algolia-api-key'] = 'a6930b815bbc3cbc03dc89b48935baa0'
        useragent['x-algolia-application-id'] = 'P7HDNSD47U'

        # HEADER = {
        #     'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8',
        #     'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        #     'x-algolia-api-key':'a6930b815bbc3cbc03dc89b48935baa0',
        #     'x-algolia-application-id':'P7HDNSD47U'
        # }

        payload = {
            "query": "",
            "getRankingInfo": False,
            "analytics": False,
            "clickAnalytics": False,
            "enableABTest": False,
            "hitsPerPage": 20,
            "attributesToRetrieve": ["context", "partnerName", "popularity", "brand", "price", "designFor_en", "productNature_en", "name_en"],
            "attributesToSnippet": [''],
            "snippetEllipsisText": "…",
            "responseFields": ["*"],
            "explain": ['*'],
            "page": i,
            "maxValuesPerFacet": 100,
            "facets": ["*"],
            "facetFilters": [["categoryIds:812b6e47-d744-4ce4-ba06-13b0ebb10780"]],
            "numericFilters": []
        }


        # Send a GET request to the URL
        response = requests.post(url, headers=useragent, json=payload)

        # print(json.dumps(response.json()['hits'][0]))

        # Extract the first hit
        # print(response.json())
        # hits = response.json()['hits']
        hits = response.json()['hits']

        if len(hits) == 0:
            print("DATA SOURCE END")
            break

        print(hits)

        hits_ls.extend(hits)
        
        time.sleep(1)

        i += 1
        
finally:
    # Write the first hit to a JSON file
#    with open('hits.json', 'w') as json_file:
#        json.dump(hits_ls, json_file, indent=4)
    producer.send('test-topic', hits_ls)
    producer.flush()    
    

