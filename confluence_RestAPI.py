import json
import requests
from requests_oauthlib import OAuth2Session

page_id = '560868319'

# Set the Confluence API endpoint and page ID
api_url = "https://kb.sprc.samsung.pl/rest/api/content/560868319"

# Set the Confluence API token and Content-Type header
api_token = "4i8c66j5q2o344ercc7kmlrq0u9mofq"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}


# Make a PUT request to update the page
response = requests.get(api_url, headers=headers, verify=False)

if response.status_code == 200:
    page_data = response.json()
    page_content = page_data["body"]["storage"]["value"]
    print(page_content)
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    print(response.text)

'''oauth = OAuth2Session(client_id=CLIENT_ID, token={'access_token': ACCESS_TOKEN})

def get_page_json(page_id, expand = False):
    if expand:
        suffix = "?expand=" + expand 
                              #body.storage
    else:
        suffix = ""

    confluence_url="https://kb.sprc.samsung.pl/rest/api/content/560868319" #+ page_id + suffix
    response = oauth.get(confluence_url)

    #response = requests.get(url, auth=(user, password))
    #response.encoding = "utf8"
    return json.loads(response.text)
    
print(get_page_json("560868319", "body.storage")) '''
