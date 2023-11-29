import requests
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
import json

project_url = "https://api.modrinth.com/v2/project/"
version_url = "https://api.modrinth.com/v2/version/"

VERSION_WANTED = "1.20.1"
LOADER_WANTED = "fabric"
DOWNLOAD_FOLDER = 'mods/'

Tk().withdraw() 
filename = askopenfilename() 


file = open("incompatible_mods.txt", "a")
file.close()
file = open("error_mods.txt", "a")
file.close()


with open(filename, "r") as read_file:
    data = json.load(read_file)['files']

    for mod in data:
        name = mod['path'][5:]
        download = mod['downloads'][0]

        # version = download[48:56]
        # url = version_url + version
        # response = requests.get(url).json()

        # if 'error' in response:
        #     response_error(url, name)
        #     continue

        # if check_version_and_loader(response):
        #     print(name + ' is compatible with version '+ VERSION_WANTED)
        #     unchanged_mods.append(name)
        #     continue

        print('Checking compatible versions of '+ name)

        project_id = download[30:38]
        url = project_url + project_id
        response = requests.get(url).json()

        if 'error' in response:
            response_error(url, name)
            continue  

        if check_version_and_loader(response):
            print(name + " doesn't have a compatible file with version "+ VERSION_WANTED)
            file = open("incompatible_mods.txt", "a")
            file.write(name)
            file.close()
            continue

        file_versions = response['versions']
        for v in file_versions[::-1]:
            url = version_url + v
            response = requests.get(url).json()

            if 'error' in response:
                response_error(url, name)
                continue

            if check_version_and_loader(response):
                download_mod(response, name)
                break


def check_version_and_loader(response):
    return not any(VERSION_WANTED in x for x in response['game_versions']) \
            and not any(LOADER_WANTED in x for x in response['loaders'])


def response_error(url, name):
    print('ERROR with url: '+ url)
    file = open("error_mods.txt", "a")
    file.write(name)
    file.close()


def download_mod(response, name):
    new_mod = response['files'][0]
    file_name = new_mod['filename']
    print('Downloading mod '+ file_name)

    url = new_mod['url'] #Download url
    response = requests.get(url)

    if not 'error' in response:
        #Save mod
        with open(DOWNLOAD_FOLDER + file_name, mode="wb") as file:
            file.write(response.content) 

        updated_mods.append(name)
    else:
        response_error(url, name)