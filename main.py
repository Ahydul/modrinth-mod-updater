import requests
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
import json

project_url = "https://api.modrinth.com/v2/project/"
version_url = "https://api.modrinth.com/v2/version/"

VERSION_WANTED = "1.20.1"
DOWNLOAD_FOLDER = 'mods/'

Tk().withdraw() 
filename = askopenfilename() 

with open(filename, "r") as read_file:
    data = json.load(read_file)['files']

    updated_mods = []
    incompatible_mods = []
    unchanged_mods = []
    mods_where_code_failed = []

    for mod in data:
        name = mod['path']
        download = mod['downloads'][0]
        version = download[48:56]
        
        url = version_url + version
        response = requests.get(url).json()

        if 'error' in response:
            print('ERROR with url: '+ url)
            mods_where_code_failed.append(name)
            continue

        mod_versions = response['game_versions']
        
        if any(VERSION_WANTED in x for x in mod_versions):
            print(name + ' is compatible with version '+ VERSION_WANTED)
            unchanged_mods.append(name)
            continue

        print('Checking compatible versions of '+ name)

        project = download[30:38]
        url = project_url + project
        response = requests.get(url).json()

        if 'error' in response:
            print('ERROR with url: '+ url)
            mods_where_code_failed.append(name)
            continue

        mod_versions = response['game_versions']

        if not any(VERSION_WANTED in x for x in mod_versions):
            print(name + " doesn't have a compatible file with version "+ VERSION_WANTED)
            incompatible_mods.append(name)
            continue

        #Checking each file from the most updated to least (reverse())
        # If it is compatible, download it and end
        file_versions = response['versions']
        for v in file_versions[::-1]:
            url = version_url + v
            response = requests.get(url).json()

            if 'error' in response:
                print('ERROR with url: '+ url)
                mods_where_code_failed.append(name)
                continue

            mod_versions = response['game_versions']

            if any(VERSION_WANTED in x for x in mod_versions):
                new_mod = response['files'][0]
                file_name = new_mod['filename']
                print('Downloading mod '+ file_name)

                url = new_mod['url'] #Download url
                response = requests.get(url)

                if 'error' in response:
                    print('ERROR with url: '+ url)
                    mods_where_code_failed.append(name)
                    break

                #Save mod
                with open(DOWNLOAD_FOLDER + file_name, mode="wb") as file:
                    file.write(response.content) 

                updated_mods.append(name)

                break
    
    file = open("update_status.txt", "w")

    file.write("Unchanged mods: \n\n")
    file.write('\n'.join(unchanged_mods))

    file.write("\n\n\nUpdated mods: \n\n")
    file.write('\n'.join(updated_mods))

    file.write("\n\nIncompatible mods: \n\n")
    file.write('\n'.join(incompatible_mods))

    file.write("\n\nError with these mods: \n\n")
    file.write('\n'.join(mods_where_code_failed))

    file.close()
