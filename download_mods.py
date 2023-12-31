import requests
import json
import os
from dotenv import load_dotenv
from move_new_mods import move_new_mods

load_dotenv()

BASE_MODRINTH = "https://api.modrinth.com/v2/version_file/{hash}/update"
BASE_CURSEFORGE = "https://api.curseforge.com/v1/mods/{mod_id}/files"
LOADERS_CURSEFORGE = {
    'fabric': 4,
    'quilt': 5,
}

COURSEFORGE_API = os.environ['COURSEFORGE_API']
DOWNLOADED_MODS = os.environ["DOWNLOADED_MODS_TXT"]
ERROR_MODS = os.environ["ERROR_MODS_TXT"]
DOWNLOAD_FOLDER = os.environ["DOWNLOAD_FOLDER"] + '/'

def reset_logs():
    file = open(ERROR_MODS, "w")
    file.close()
    with open(DOWNLOADED_MODS, "w") as file:
        file.write("old mod"+','+'new mod'+'\n')

def response_error(url, file_name):
    print('ERROR with url: '+ url)
    with open(ERROR_MODS, "a") as file:
        file.write(file_name+'\n')


def download_mod(url, file_name, old_name, source):
    print('Downloading mod '+ file_name)
    response = requests.get(url)

    if not 'error' in response:
        #Save mod
        with open(DOWNLOAD_FOLDER + file_name, mode="wb") as file:
            file.write(response.content) 

        with open(DOWNLOADED_MODS, "a") as file:
            file.write(old_name+','+file_name+'\n')
    else:
        response_error(url, old_name)


def download_mods(version_wanted, loader_wanted, mods):
    for mod in mods:
        filename = mod['file']
        print("Checking updates for: "+ mod['name'])

        #If its a modrinth mod
        if "modrinthVersion" in mod:
            mod_files = mod['modrinthVersion']['files']

            #We get the mod_file with the filename we have and we get its hash
            hash = next(filter(lambda m: m['filename'], mod_files), None)['hashes']['sha512']

            url = BASE_MODRINTH.replace("{hash}", hash)
            params = {
                'algorithm':"sha512"
            }
            data = {
                "loaders": [loader_wanted],
                "game_versions": [version_wanted],
            }

            response = requests.post(url, json=data, params=params)
            if response.status_code!=200:
                response_error(url, filename)
                continue

            file = response.json()['files'][0]
            download_url = file['url']
            new_filename = file['filename']

            #Skip if the file is the same
            if new_filename == filename:
                continue

            download_mod(download_url, new_filename, filename, 'modrinth')

        else: #If curseforge mod
            mod_id = mod['curseForgeProjectId']

            url = BASE_CURSEFORGE.replace("{mod_id}", str(mod_id))
            params = {
                "modLoaderType": LOADERS_CURSEFORGE[loader_wanted],
                "gameVersion": version_wanted,
            }
            headers = {
                'Accept': 'application/json',
                'x-api-key': COURSEFORGE_API,
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code!=200:
                response_error(url, filename)
                continue

            file = response.json()['data'][0]
            download_url = file['downloadUrl']
            new_filename = file['fileName']

            #Skip if the file is the same
            if new_filename == filename:
                continue

            download_mod(download_url, new_filename, filename, 'curseforge')


def update_mods(instance_folder): 
    reset_logs()  

    with open(instance_folder+'/instance.json', "r") as read_file:
        data = json.load(read_file)['launcher']
        version_wanted = data['version']
        loader_wanted = data['loaderVersion']['type'].lower()

        condition = lambda m: m['type'] == 'mods' and m['disabled'] == False
        mods = filter(condition, data['mods'])

    download_mods(mods=mods, version_wanted=version_wanted, loader_wanted=loader_wanted)

    move_new_mods(instance_folder=instance_folder)


def update_error_mods(instance_folder): 
    mod_errors = []
    with open(ERROR_MODS, "r") as file:
        for line in file:
            mod_errors.append(line.replace('\n',''))

    reset_logs()  

    with open(instance_folder+'/instance.json', "r") as read_file:
        data = json.load(read_file)['launcher']
        version_wanted = data['version']
        loader_wanted = data['loaderVersion']['type'].lower()

        condition = lambda m: m['type'] == 'mods' and m['disabled'] == False and  \
                            m['file'] in mod_errors
        mods = filter(condition, data['mods'])

    download_mods(mods=mods, version_wanted=version_wanted, loader_wanted=loader_wanted)

    move_new_mods(instance_folder=instance_folder)

