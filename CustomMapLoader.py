#!/usr/bin/python

import sys
import os
import json
from shutil import copyfile

args = sys.argv[1:]
if (os.path.isfile(os.path.expanduser('~/.custommaploaderrc'))):
    with open(os.path.expanduser('~/.custommaploaderrc'), 'r') as json_data_file:
        config_data = json.load(json_data_file)
else:
    config_data = {'mapsPath': '', 'gamePath': ''}


def printHelp():
    print('Usage: custommaploader [--help] {setup,setmap,list}')
    print()
    print('custommaploader setup')
    printSetupHelp()
    print()
    print('custommaploader setmap')
    printSetmapHelp()


def printSetupHelp():
    print('Usage: custommaploader setup {maps,rocketleague} (path/to/folder)')
    print('\tRocket League folder should be something like ~/.local/share/Steam/steamapps/common/rocketleague')
    print('\tMaps folder should contain folders of custom maps')


def printSetmapHelp():
    print('Usage: custommaploader setmap (map name)')
    print('\tAvailable maps can be found with custommaploader list')


def checkPath(type):
    if (config_data[type + 'Path'] == ''):
        print('Error: Path for', type, 'has not been setup yet')
        printSetupHelp()
        exit()
    if (not os.path.isdir(config_data[type + 'Path'])):
        print('Error: The stored', type,
              'path (', config_data[type + 'Path'], ') no longer exists')
        print('You\'ll need to re-run the setup command for', type)
        printSetupHelp()
        exit()


def checkValidMap(map):
    mapPath = config_data['mapsPath'] + '/' + map
    if (not os.path.isdir(mapPath)):
        print('Error: Couldn\'t find the map folder for', map)
        exit()
    mapFileCount = 0
    for f in os.listdir(mapPath):
        if (f.endswith('.udk') or f.endswith('.upk')):
            mapFileCount += 1
    if (mapFileCount == 0):
        print('Error: Couldn\'t find any map files (*.udk, *.upk) in the map folder')
        exit()
    if (mapFileCount > 1):
        print('Error: Found more than 1 map file (*.udk, *.upk) in the map folder (found', mapFileCount + ')')
        exit()


def backupUnderpass():
    cookedPath = config_data['gamePath'] + '/TAGame/CookedPCConsole'
    if (not os.path.isdir(cookedPath)):
        print('Error: Couldn\'t find folder TAGame/CookedPCConsole in',
              config_data['gamePath'])
        print('This folder is critical to Rocket League to function, ensure you have setup the proper folder')
        printSetupHelp()
        exit()
    if (not os.path.isfile(cookedPath + '/Labs_Underpass_P.upk')):
        print('Warning: Couldn\'t find the Underpass map to backup, continuing anyway')
    else:
        if (not os.path.isfile(cookedPath + '/Labs_Underpass_P_BACKUP.upk')):
            os.rename(cookedPath + '/Labs_Underpass_P.upk',
                      cookedPath + '/Labs_Underpass_P_BACKUP.upk')


def getMapFilePath(mapName):
    folderPath = config_data['mapsPath'] + '/' + mapName
    for f in os.listdir(folderPath):
        if (f.endswith('.udk') or f.endswith('.upk')):
            return folderPath + '/' + f
    return ''


if (len(args) == 0 or (args[0] == '--help' and len(args) == 1)):
    printHelp()
    exit()

if (args[0] == 'setup'):
    if (len(args) == 2 or (args[1] != 'maps' and args[1] != 'rocketleague') or '--help' in args):
        printSetupHelp()
        exit()

    path = os.path.abspath(' '.join(args[2:]))
    if (not os.path.isdir(path)):
        print('Error:', path, 'is not a valid directory')
        printSetupHelp()
        exit()

    if (args[1] == 'maps'):
        config_data['mapsPath'] = path
    else:
        config_data['gamePath'] = path

    with open(os.path.expanduser('~/.custommaploaderrc'), 'w') as outfile:
        json.dump(config_data, outfile)

    print('Path for', args[1], 'set to', path)
    exit()

if (args[0] == 'list'):
    checkPath('maps')
    path = os.path.abspath(config_data['mapsPath'])

    print('The following maps are available for selection')
    for name in sorted(os.listdir(path)):
        newPath = path + '/' + name
        if (os.path.isdir(newPath)):
            for innerFile in os.listdir(newPath):
                if (innerFile.endswith('.udk') or innerFile.endswith('.upk')):
                    print(name)
                    break
    if (os.path.isfile(config_data['gamePath'] + '/TAGame/CookedPCConsole/Labs_Underpass_P_BACKUP.upk')):
        print('Underpass (reset to vanilla)')
    exit()

if (args[0] == 'setmap'):
    checkPath('maps')
    checkPath('game')
    if (len(args) == 1 or '--help' in args):
        printSetmapHelp()
        exit()
    mapName = ' '.join(args[1:])
    cookedPath = config_data['gamePath'] + '/TAGame/CookedPCConsole'
    if (mapName == 'Underpass'):
        if (os.path.isfile(cookedPath + '/Labs_Underpass_P_BACKUP.upk')):
            os.replace(cookedPath + '/Labs_Underpass_P_BACKUP.upk',
                       cookedPath + '/Labs_Underpass_P.upk')
            print('The Underpass map has been restored to vanilla')
        else:
            print('Error: No backup Underpass to restore from')
        exit()
    checkValidMap(mapName)
    backupUnderpass()
    mapPath = getMapFilePath(mapName)
    copyfile(mapPath, cookedPath + '/Labs_Underpass_P.upk')
    print('The', mapName, 'map has been loaded, replacing Underpass')
