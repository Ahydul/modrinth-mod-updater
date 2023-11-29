import os
from os import listdir
from os.path import isfile, join

path = '/home/ahydul/.var/app/com.atlauncher.ATLauncher/data/instances/Minecraft1201withFabric/mods'
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]


file = open("update_status.txt", "r")
updated_mods = False
for mod in file:
    if 'Incompatible mods:' in mod:
        break

    if updated_mods:
        file = path+'/'+mod.replace('\n','')
        print('Deleting: '+file)
        if os.path.isfile(file):
            os.remove(file)
        else:
            print("Error: %s file not found" % file)

    if 'Updated mods:' in mod:
        updated_mods = True

file.close()
