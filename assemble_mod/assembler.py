#! python3

import json
import os
import shlex
import subprocess


def run(directory, **args):
    path = os.path
    here = os.getcwd()
    directory = path.abspath(directory)

    with open(path.join(directory, "info.json"), "r") as info_json:
        info = json.load(info_json)

    id = "{}_{}".format(info['name'], info['version'])
    cache = path.join(here, ".cache", info['name'])
    config = path.join(cache, "config", "config.ini")
    mod = path.join(cache, "mods", id)

    if args['deploy']:
        subprocess.run(
            shlex.split(
                "git archive HEAD --prefix={0}/ -o ../{0}.zip".format(id)),
            cwd=directory)
        print(os.path.abspath("{0}.zip".format(id)))
        return

    os.makedirs(path.dirname(config), exist_ok=True)
    if not path.exists(config):
        with open(config, "w") as cf:
            cf.writelines("""; version=3
[path]
read-data=__PATH__executable__/../../data
write-data={0}

[graphics]
graphics-quality=normal
full-screen=false
force-opengl=true
video-memory-usage=medium
""".format(cache))

    os.makedirs(path.dirname(mod), exist_ok=True)
    for entry in os.scandir(path.dirname(mod)):
        if entry.is_symlink():
            os.unlink(entry.path)
    os.symlink(directory, mod)

    arguments = [
        path.join(here, info['factorio_version'], 'bin', 'x64', 'factorio'),
        '--mod-directory',
        path.dirname(mod), '--config', config, '--enable-runtime-autoplace-modification'
    ]
    subprocess.run(arguments)


def abort():
    pass
