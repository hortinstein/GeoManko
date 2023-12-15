#!/usr/bin/env python
# coding: utf-8

# ### GeoManko
# 
# To get started, ensure you have an [API key from here](https://developers.google.com/maps) or maybe [here](https://console.cloud.google.com/google/maps-apis/credentials) if you cannot find it...im logged in so i cant see: I will use the following API to get return the location given the SSID keys https://developers.google.com/maps/documentation/geolocation/requests-geolocation#wifi_access_point_object

# ### Install Python libraries
# 
# Run the following command (minus the exclamation portion in a terminal) or run this cell in the notebook

# In[7]:


# ### Load your api key
# 
# This will load the API key, before editing it, ensure you change the ```"your_api_key"``` or create a ```.env``` file with the key in the format ```API_KEY="MY_KEY"```

# In[ ]:


import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Set default API key value
default_api_key = "your_api_key"

# Read API key from .env file or use the default
api_key = os.getenv('API_KEY', default_api_key)

print("API Key:", api_key)


# ### Get the test data
# 
# The following code retrieves the input data for the problem

# In[8]:


import requests

# URL of the JSON data
json_url = "https://metaproblems.com/0d96db28b305a8f2504d7a9f9be044c0/phonedata.json"

# Making a request to get the JSON data
response = requests.get(json_url)

# Checking if the request was successful
if response.status_code == 200:
    # Parsing the JSON data
    json_data = response.json()
else:
    json_data = None
    print("Failed to retrieve data. Status code:", response.status_code)

# Use json_data as needed
json_data


# ### Create the request
# 
# I need to put the data in a format shown by the [documentation](https://developers.google.com/maps/documentation/geolocation/requests-geolocation#wifi_access_point_object)
# 
# and then create the request and print out the result

# In[12]:


import json 

def convert_key_names(json_data, old_key, new_key):
    """
    Converts specified key names in a JSON object.

    :param json_data: A JSON object (dict in Python) that may contain the old_key.
    :param old_key: The key name to be replaced.
    :param new_key: The new key name to replace old_key.
    :return: A new JSON object with old_key replaced by new_key.
    """
    if isinstance(json_data, dict):
        return {new_key if key == old_key else key: convert_key_names(value, old_key, new_key) for key, value in json_data.items()}
    elif isinstance(json_data, list):
        return [convert_key_names(item, old_key, new_key) for item in json_data]
    else:
        return json_data

wrapped_data = {
    "considerIp": "false",
    "wifiAccessPoints": json_data
}

#convert the names to match googles API
wrapped_data= convert_key_names(wrapped_data,'bssid','macAddress')
wrapped_data= convert_key_names(wrapped_data,'rssi','signalStrength')

# URL for the Google Geolocation API
url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"

# Make the POST request
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(wrapped_data))

# Print response (or handle it as needed)
print(response.status_code)
print(response.text)

