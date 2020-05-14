import requests
import json
url = 'https://www.trustpilot.com/businessunit/5da0abed5cd86d000153ccbd/companyinfobox'
response = requests.get(url)
responseActivityBox = json.loads(response.text)
print(responseActivityBox['categories'][0]['breadcrumb']['localizedName'])
