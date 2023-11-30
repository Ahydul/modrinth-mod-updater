import requests
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
import json

version_url = "https://api.modrinth.com/v2/version/"
# BASE = "https://api.modrinth.com/v2/version_file/{hash}/update"

VERSION_WANTED = ["1.20.1"]
LOADER_WANTED = ["fabric"]
DOWNLOAD_FOLDER = 'mods/'


file = open("error_mods.txt", "w")
file.close()

file = open("updated_mods.txt", "w")
file.write("old mod"+','+'new mod'+'\n')
file.close()

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


# Tk().withdraw() 
# filename = askopenfilename() 
filename = "/home/ahydul/Documents/Programming/VSCode/modrinth-mod-updater/modrinth.index.json"

projectid_versionid_we_have = set()

dependencies_projectid = set() #If only projectid is required
dependencies_projectid_versionid = set() #If both are required

with open(filename, "r") as read_file:
    data = json.load(read_file)['files']
    for mod in data:

        version_id = mod['downloads'][48:56]
        project_id = mod['downloads'][30:38]

        projectid_versionid_we_have(
        {
            'name': name,
            'version_id': version_id,
            'project_id': project_id,
        })


for mod in projectid_versionid_we_have:
    name = mod['name']
    version_id = mod['version_id']
    project_id = mod['project_id']
    
    print("Checking dependencies for: "+ name)

    url = version_url + version_id

    response = requests.get(url)
    if not 'error' in response:
        response_error(url, name)
        continue

    dependencies = response.json()['dependencies']
    for d in dependencies:
        if d['dependency_type'] != 'required':
            continue

        if d['version_id'] == None:
            #Ignore if we already have this mod
            if(not any(mod2['project_id'] == d['project_id'] for mod2 in projectid_versionid_we_have)):
                dependencies_projectid.append(d['project_id'])

        #In this case it needs a specific version of a mod, we check if we have it
        else :
            

            dependencies_projectid.append([ d['version_id'], d['project_id'] ])


download_url = file['url']
file_name = file['filename']

#Skip if the file is the same
if file_name == name:
    continue

download_mod(download_url, file_name, name)
        
