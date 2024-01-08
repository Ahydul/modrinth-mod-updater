import os

#Folder where mods will be downloaded to 
os.environ["DOWNLOAD_FOLDER"] = "mods"

#Name of logs used and created in the scripts
os.environ["DOWNLOADED_MODS_TXT"] = "downloaded_mods.txt" 
os.environ["ERROR_MODS_TXT"] = "error_mods.txt"
os.environ["UPDATED_MODS_TXT"] = "updated_mods.txt"

from download_mods import update_mods  
from download_mods import update_error_mods  



instance_folder = '/home/ahydul/.local/share/atlauncher/instances/CHANGETOQUILT'

if not os.path.exists(instance_folder): #path should exist
    exit(1)

update_mods(instance_folder=instance_folder)
