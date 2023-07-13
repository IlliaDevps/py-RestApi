# This code sample uses the Confluence RestAPI:
# Created by Illia Duverkher-Natiahin

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json

urllib3.disable_warnings()

url = "https://kb.sprc.samsung.pl/rest/api/content/"
auth = HTTPBasicAuth ("i.duverkher", "4i8c66j5q2o344ercc7kmlrq0u9mofq")


def get_page_json(page_id, expand=False):
    if expand:
        suffix = "?expand=" + expand
        # body.storage or body.view
    else:
        suffix = ""

    url = f"https://kb.sprc.samsung.pl/rest/api/content/{page_id}" + suffix

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth,
        verify=False
    )
    response.encoding = "utf8"
    json_data = json.loads(response.text)
    # json_data = json.dumps(json.loads(response.text),sort_keys=True, indent=4, separators=(",", ": "))
    # print(json_data['body']['storage']['value'])

    return json_data  # ['body']['storage']['value']


#print(get_page_json("563617140", 'body.storage'))  # Iza page_id is 560881462


def get_and_set(page_id):
    json_data = get_page_json(page_id)

    fname = "myconfluence.html" # this is the name of my html file
    html_file = open(fname, 'r', encoding='utf-8')
    html_source_code = html_file.read()  
    print(html_source_code)

    macro_content = f'''
                    <!-- BEGIN HTML Macro -->
                    <ac:structured-macro ac:name="html">
                        <ac:plain-text-body>
                            <![CDATA[
                                {html_source_code}
                            ]]>
                        </ac:plain-text-body>
                    </ac:structured-macro>
                    <!-- END HTML Macro -->
                    '''
                   

    new_json_data = dict()
    new_json_data['id'] = json_data['id']
    new_json_data['type'] = json_data['type']
    new_json_data['title'] = json_data['title']
    new_json_data['type'] = json_data['type']
    new_json_data['version'] = {"number": json_data['version']['number'] + 1}
    if not 'key' in json_data:
        new_json_data['key'] = json_data['space']['key']
    else:
        new_json_data['key'] = json_data['key']

    new_json_data['body'] = {'storage': {
                            'value': macro_content , 
                            'representation': 'storage'}}
    print(set_page_json(page_id, new_json_data))


def set_page_json(page_id, json_content):
    url = f"https://kb.sprc.samsung.pl/rest/api/content/{page_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "PUT",
        url,
        data=json.dumps(json_content),
        headers=headers,
        auth=auth,
        verify=False
    )

    if response.status_code == 200:
        print('HTML macro created successfully.')
    else:
        print('Failed to create HTML macro. Error:', response.text)


print(get_and_set('563617140'))  # 563617140 confluence testing page
