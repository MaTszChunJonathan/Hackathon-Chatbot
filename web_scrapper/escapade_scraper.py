import requests
from bs4 import BeautifulSoup
import json
import re

# URL to fetch
url = 'https://zh.escapade.com.hk/search?q=cycling'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the script tag with the specific ID
    script_tag = soup.find('script', {'id': 'web-pixels-manager-setup'})
    
    pattern = r'\[\{\"price\":.*?\}\]'

    # Search for the pattern
    matches = re.findall(pattern, str(script_tag))

    json_data = json.loads(matches[0])

    with open('output.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")