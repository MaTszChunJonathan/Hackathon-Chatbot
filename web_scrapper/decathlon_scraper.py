import requests
import json
from masquer import masq
import time
import argparse

def scrape_decathlon(category_id):
    url = "https://p7hdnsd47u-dsn.algolia.net/1/indexes/prod_pim_v1_index/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.15.0)%3B%20Browser%20(4.15.0)"

    hits_ls = list()

    i = 0
    try:
        while True: # just scrape until it has nothing in hits
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
                "facetFilters": [[f"categoryIds:{category_id}"]],
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

            hits_ls.extend(hits)
            
            time.sleep(1)

            i += 1
            
    finally:
        # Write the first hit to a JSON file
        with open('hits.json', 'w') as json_file:
            json.dump(hits_ls, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape data for a given category ID.')
    parser.add_argument('category_id', type=str, help='The category ID to scrape data from')

    args = parser.parse_args()
    scrape_decathlon(args.category_id)
    
    
    # "all": "categoryIds:812b6e47-d744-4ce4-ba06-13b0ebb10780"
    # "bike": "categoryIds:f28ec0c7-ce32-4184-abdd-a524d3d7a344"
    # "Hiking_And_Trekking": "categoryIds:3e067cd4-1a2e-421d-8d67-362fe60252ae": 
    # "Climbing_And_Moutaineering": "categoryIds:5702040d-c923-4991-99d8-ad623241e2f5"
    
    # python3 decathlon_scraper.py 812b6e47-d744-4ce4-ba06-13b0ebb10780
    # python3 decathlon_scraper.py f28ec0c7-ce32-4184-abdd-a524d3d7a344
    # python3 decathlon_scraper.py 3e067cd4-1a2e-421d-8d67-362fe60252ae
    # python3 decathlon_scraper.py 5702040d-c923-4991-99d8-ad623241e2f5