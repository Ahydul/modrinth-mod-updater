import os, shutil
from os import listdir
from os.path import isfile, join

# Tk().withdraw() 
# mods_path = askopenfilename() 
mods_path = '/home/ahydul/.var/app/com.atlauncher.ATLauncher/data/instances/Minecraft1201withFabric/mods'

file = open("updated_mods.txt", "r")

skip_first = True
for line in file:
    if skip_first:
        skip_first = False
        continue

    spl = line.split(',')
    old_mod = spl[0]
    new_mod = spl[1].replace('\n','')

    delete_file = mods_path+'/'+old_mod
    copy_file = 'mods/'+new_mod

    if not os.path.isfile(delete_file):
        print("Error: %s file not found" % delete_file)
        continue
    if not os.path.isfile(copy_file):
        print("Error: %s file not found" % copy_file)
        continue

    print('Copying: ' + copy_file + ' to '+ mods_path)
    #src, dst
    shutil.copy(copy_file, mods_path)

    print('Deleting: ' + delete_file)
    os.remove(delete_file)

    print('Deleting: ' + copy_file)
    os.remove(copy_file)


file.close()
