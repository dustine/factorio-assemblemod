#! python3

import os
import json
import subprocess


def run(directory, **args):
    path = os.path
    here = os.getcwd()
    directory = path.abspath(directory)

    with open(path.join(directory, "info.json"), "r") as info_json:
        info = json.load(info_json)
    print(args)
    print(info)

    cache = path.join(here, ".cache", info['name'])
    config = path.join(cache, "config", "config.ini")
    mod = path.join(cache, "mods", "{0}-{1}".format(info['name'],
                                                    info['version']))

    os.makedirs(path.dirname(config), exist_ok=True)
    if not path.exists(config):
        with open(config, "w") as cf:
            cf.writelines("""; version=2
[path]
read-data=__PATH__executable__/../../data
write-data={0}

[graphics]
graphics-quality=normal""".format(cache))

    os.makedirs(path.dirname(mod), exist_ok=True)
    for entry in os.scandir(path.dirname(mod)):
        if entry.is_symlink():
            os.unlink(entry.path)
    os.symlink(directory, mod)

    arguments = [
        path.join(here, info['factorio_version'], 'bin', 'x64', 'factorio'),
        '-- mod-directory',
        path.dirname(mod),
        '--config',
        config
    ]
    # if path.exists(path.join(mods, )):
    result = subprocess.run(arguments, shell=True)
    print(result)
    pass


def abort():
    pass
