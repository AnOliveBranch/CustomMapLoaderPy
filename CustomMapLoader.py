#!/usr/bin/python

import sys
import os
import json

args = sys.argv[1:]
if (os.path.isfile(os.path.expanduser('~/.custommaploaderrc'))):
    with open(os.path.expanduser('~/.custommaploaderrc'), 'r') as json_data_file:
        config_data = json.load(json_data_file)
else:
    config_data = {'mapsPath': '', 'gamePath': ''}


def printHelp():
    print('Usage: custommaploader [--help] {setup,list,setmap}')
    print()
    print('custommaploader setup')
    printSetupHelp()


def printSetupHelp():
    print('Usage: custommaploader setup {maps,rocketleague} (path/to/folder)')
    print('\tRocket League folder should be something like ~/.local/share/Steam/steamapps/common/rocketleague')
    print('\tMaps folder should contain folders of custom maps')


if (len(args) == 0 or (args[0] == '--help' and len(args) == 1)):
    printHelp()
    exit()

if (args[0] == 'setup'):
    if (len(args) == 2 or (args[1] != 'maps' and args[1] != 'rocketleague')):
        printSetupHelp()
        exit()

    path = ' '.join(args[2:])
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
    if (config_data['mapsPath'] == ''):
        print('Path for maps has not been setup yet')
        printSetupHelp()
        exit()
    if (not os.path.isdir(config_data['mapsPath'])):
        print('The stored maps path no longer exists')
        printSetupHelp()
        exit()
    path = os.path.abspath(config_data['mapsPath'])

    print('The following maps are available for selection')
    for name in sorted(os.listdir(path)):
        newPath = path + '/' + name
        if (os.path.isdir(newPath)):
            for innerFile in os.listdir(newPath):
                if (innerFile.endswith('.udk') or innerFile.endswith('.upk')):
                    print(name)
    print('Underpass (reset to vanilla)')
    exit()
