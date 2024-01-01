import requests
import json

project_url = "https://api.modrinth.com/v2/project/"
version_url = "https://api.modrinth.com/v2/version/"
BASE = "https://api.modrinth.com/v2/version_file/{hash}/update"
DOWNLOAD_FOLDER = 'mods/'

def response_error(url, name):
    print('ERROR with url: '+ url)
    file = open("error_mods.txt", "a")
    file.write(name+'\n')
    file.close()


def download_mod(url, file_name, old_name):
    print('Downloading mod '+ file_name)
    response = requests.get(url)

    if not 'error' in response:
        #Save mod
        with open(DOWNLOAD_FOLDER + file_name, mode="wb") as file:
            file.write(response.content) 
        #Update updated_mods.txt
        file = open("updated_mods.txt", "a")
        file.write(old_name+','+file_name+'\n')
        file.close()
    else:
        response_error(url, name)


def download_mods(instance_folder, filename):
    version_wanted = []
    loader_wanted = []
    with open(instance_folder+'/instance.json', "r") as read_file:
        data = json.load(read_file)['launcher']
        version_wanted.append(data['version'])
        loader_wanted.append(data['loaderVersion']['type'].lower())

    file = open("error_mods.txt", "w")
    file.close()

    file = open("updated_mods.txt", "w")
    file.write("old mod"+','+'new mod'+'\n')
    file.close()


    with open(filename, "r") as read_file:
        data = json.load(read_file)['files']

        for mod in data:
            name = mod['path'][5:]
            print("Checking updates for: "+ name)
            hash = mod['hashes']['sha512']

            url = BASE.replace("{hash}", hash)
            params = {
                'algorithm':"sha512"
            }
            data = {
                "loaders": loader_wanted,
                "game_versions": version_wanted,
            }

            response = requests.post(url, json=data, params=params)
            if response.status_code!=200:
                response_error(url, name)
                continue

            file = response.json()['files'][0]
            download_url = file['url']
            file_name = file['filename']

            #Skip if the file is the same
            if file_name == name:
                continue

            download_mod(download_url, file_name, name)
            
