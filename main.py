import os
from download_mods import update_mods  
from download_mods import update_error_mods  

instance_folder = '/home/ahydul/.local/share/atlauncher/instances/Minecraft1201withFabric'

if not os.path.exists(instance_folder): #path should exist
    exit(1)

update_error_mods(instance_folder=instance_folder)
