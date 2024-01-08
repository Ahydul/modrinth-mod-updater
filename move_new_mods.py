import os, shutil
from os import listdir
from os.path import isfile, join

def error(msg, file_name, txt):
    print(msg)
    with open(txt, "a") as file:
        file.write(file_name+'\n')

def move_new_mods(instance_folder):
    mods_path = instance_folder + '/mods'
    updater_folder = instance_folder + '/updater'

    backup_mods_path = updater_folder + '/old_mods'
    updated_mods_logs = updater_folder + '/updated_mods_logs.txt'
    error_mods_logs = updater_folder + '/error_mods_logs.txt'
    downloaded_mods_logs = updater_folder + '/downloaded_mods_logs.txt'

    if os.path.exists(backup_mods_path): #backup_mods_path must exist
        shutil.rmtree(backup_mods_path)

    #Create logs in instance
    with open(updated_mods_logs, "w") as file:
        file.write("old mod,new mod\n")
    shutil.copy("error_mods.txt", error_mods_logs)
    shutil.copy("downloaded_mods.txt", downloaded_mods_logs)

    print("Making backup of mods into /old_mods")
    shutil.copytree(mods_path, backup_mods_path) 

    move_mods(mods_path=mods_path, backup_mods_path=backup_mods_path, updated_mods_logs=updated_mods_logs,error_mods_logs=error_mods_logs)

def move_mods(mods_path, backup_mods_path, updated_mods_logs, error_mods_logs):
    with open("downloaded_mods.txt", "r") as file:
        next(file) #skip first row

        for line in file:
            spl = line.split(',')
            old_mod = spl[0]
            new_mod = spl[1].replace('\n','')

            delete_file = mods_path+'/'+old_mod
            destination = backup_mods_path+'/'+old_mod
            copy_file = 'mods/'+new_mod

            if not os.path.isfile(delete_file):
                error("Error: %s file not found" % delete_file, old_mod, error_mods_logs)
                continue
            if not os.path.isfile(copy_file):
                error("Error: %s file not found" % copy_file, old_mod, error_mods_logs)
                continue

            print('\n')

            print('Copying ' + copy_file + ' to '+ mods_path)
            shutil.copy(copy_file, mods_path)
            with open(updated_mods_logs, "a") as file:
                file.write(old_mod+','+new_mod+'\n')

            print('Deleting ' + delete_file)
            shutil.move(delete_file, destination)

            print('Deleting ' + copy_file)
            os.remove(copy_file)

