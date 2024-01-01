import os
import download_mods
import move_new_mods

modrinth_mods = "/home/ahydul/Documents/Programming/VSCode/modrinth-mod-updater/modrinth.index.json"
instance_folder = '/home/ahydul/.local/share/atlauncher/instances/Minecraft1201withFabric'

if not os.path.exists(instance_folder) or not os.path.exists(modrinth_mods): #path should exist
    exit(1)

download_mods.download_mods(filename=modrinth_mods, instance_folder=instance_folder)
move_new_mods.move_new_mods(instance_folder=instance_folder)