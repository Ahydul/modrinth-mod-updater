import os, shutil
from os import listdir
from os.path import isfile, join

def move_new_mods(instance_folder):
    mods_path = instance_folder + '/mods'
    backup_mods_path = instance_folder + '/old_mods'

    if os.path.exists(backup_mods_path): #backup_mods_path must exist
        shutil.rmtree(backup_mods_path)

    print("Making backup of mods into /old_mods")
    shutil.copytree(mods_path, backup_mods_path) 

    file = open("updated_mods.txt", "r")
    next(file) #skip first row

    for line in file:
        spl = line.split(',')
        old_mod = spl[0]
        new_mod = spl[1].replace('\n','')

        delete_file = mods_path+'/'+old_mod
        destination = backup_mods_path+'/'+old_mod
        copy_file = 'mods/'+new_mod

        if not os.path.isfile(delete_file):
            print("Error: %s file not found" % delete_file)
            continue
        if not os.path.isfile(copy_file):
            print("Error: %s file not found" % copy_file)
            continue

        print('\n\n')

        print('Copying ' + copy_file + ' to '+ mods_path)
        shutil.copy(copy_file, mods_path)

        print('Deleting ' + delete_file)
        shutil.move(delete_file, destination)

        print('Deleting ' + copy_file)
        os.remove(copy_file)

        print('\n\n')


    file.close()
