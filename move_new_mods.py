import os, shutil
from os import listdir
from os.path import isfile, join

ERROR_MODS = os.environ["ERROR_MODS_TXT"]
DOWNLOADED_MODS = os.environ["DOWNLOADED_MODS_TXT"]
DOWNLOAD_FOLDER = os.environ["DOWNLOAD_FOLDER"] + '/'
UPDATED_MODS = os.environ["UPDATED_MODS_TXT"]

def error(msg, file_name, txt):
    print(msg)
    with open(txt, "a") as file:
        file.write(file_name+'\n')

def move_new_mods(instance_folder):
    mods_path = instance_folder + '/' + DOWNLOAD_FOLDER
    updater_folder = instance_folder + '/updater'

    backup_mods_path = updater_folder + '/old_mods/'
    updated_mods_logs = updater_folder + '/' + UPDATED_MODS
    error_mods_logs = updater_folder + '/' + ERROR_MODS
    downloaded_mods_logs = updater_folder + '/' + DOWNLOADED_MODS

    if os.path.exists(backup_mods_path):
        shutil.rmtree(backup_mods_path) #Delete /old_mods if it exists

    #Backup mods
    shutil.copytree(mods_path, backup_mods_path) 

    #Create logs in instance
    with open(updated_mods_logs, "w") as file:
        file.write("old mod,new mod\n")
    shutil.copy(ERROR_MODS, error_mods_logs)
    shutil.copy(DOWNLOADED_MODS, downloaded_mods_logs)


    move_mods(mods_path=mods_path, backup_mods_path=backup_mods_path, updated_mods_logs=updated_mods_logs,error_mods_logs=error_mods_logs)

def move_mods(mods_path, backup_mods_path, updated_mods_logs, error_mods_logs):
    with open(DOWNLOADED_MODS, "r") as file:
        next(file) #skip first row

        for line in file:
            spl = line.split(',')
            old_mod = spl[0]
            new_mod = spl[1].replace('\n','')

            delete_file = mods_path + old_mod
            destination = backup_mods_path + old_mod
            copy_file = DOWNLOAD_FOLDER + new_mod

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

