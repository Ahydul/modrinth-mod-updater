import requests
import json

url = 'https://api.modrinth.com/v2/version/hCsMUZLa'

response = requests.get(url)
if not 'error' in response:
    dependencies = response.json()['dependencies']
    for d in dependencies:
        if d['dependency_type'] == 'required':
            if d['version_id'] == None:
                print(d['project_id'])
            else :
                print(d['version_id']+'\n')
                print(d['project_id'])
else:
    print('error')
