#! python3

import configparser
import json
import logging
import os
import shutil
import subprocess
import sys

import colorama
# import semver

path = os.path
Fore = colorama.Fore

colorama.init(autoreset=True)


def run(directory, verbose, **args):
    source = os.getcwd()
    # directory = path.abspath(directory)

    # load mod's info.json
    info_path = path.join(directory, "info.json")
    with open(info_path, "r") as fi:
        info = json.load(fi)
    logging.info("Loaded %s, %s%s v%s%s for Factorio %s", info_path, Fore.CYAN,
                 info['name'], info['version'], Fore.RESET,
                 info['factorio_version'])
    logging.debug(info)

    # find target factorio and load its info.json
    if source in args:
        source = args['source']
        # fail deadly if it's an invalid source
        factorio_path = path.join(source, source,
                                  'factorio-' + info['factorio_version'])
    else:
        source = os.getcwd()
        while source:
            logging.debug(source)
            factorio_path = path.join(source,
                                      'factorio-' + info['factorio_version'])
            factorio_info_path = path.join(factorio_path, 'data', 'base',
                                           'info.json')
            if path.exists(factorio_info_path) or source == path.dirname(
                    source):
                break
            source = path.dirname(source)

    with open(path.join(factorio_path, 'data', 'base', 'info.json')) as fif:
        factorio_info = json.load(fif)
    logging.info("Loaded Factorio %s", factorio_info['version'])
    logging.debug("Factorio base info: %s", factorio_info)

    id = "{}_{}".format(info['name'], info['version'])
    cache_path = path.join(source, ".cache", info['name'])
    config_path = path.join(cache_path, "config", "config.ini")
    mod_path = path.join(cache_path, "mods", id)

    # reset
    # mod symbolic link
    if path.exists(path.dirname(mod_path)):
        for entry in os.scandir(path.dirname(mod_path)):
            if entry.name.startswith(info['name']):
                os.remove(entry.path)
                logging.debug("Removed mod link %s", entry.path)

    if args['reset']:
        # 1:  remove config
        # 2:  1 + remove all mods
        # 3+: remove *everything* from the cache
        if args['reset'] > 2 and path.exists(cache_path):
            shutil.rmtree(cache_path)
            logging.info("Cache wiped out")
        else:
            if path.exists(config_path):
                os.remove(config_path)
                logging.info("Config file removed")
            if args['reset'] > 1 and path.exists(path.dirname(mod_path)):
                shutil.rmtree(path.dirname(mod_path))
                logging.info("Cached mods removed")

    # deploy (create zip)
    if args['deploy']:
        deploy_path = path.join(source, "{}.zip".format(id))
        result = subprocess.run(
            [
                'git', 'archive', 'HEAD', '--prefix={}/'.format(id), '-o',
                deploy_path
            ],
            cwd=directory)

        if result.returncode == 0:
            logging.info("Created HEAD deployable {}".format(deploy_path))
            print(Fore.GREEN +
                  "Created {}".format(path.abspath("{}.zip".format(id))))
        return

    # (re)create config
    os.makedirs(path.dirname(config_path), exist_ok=True)
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        with open(config_path, 'r') as cf:
            config.read_file(cf)
            logging.info("Config file created")
    if not config.has_section('path'):
        config.add_section('path')
    config['path']['read-data'] = "__PATH__executable__/../../data"
    config['path']['write-data'] = cache_path

    if not config.has_section('graphics'):
        config.add_section('graphics')
    graphics = config['graphics']
    if 'graphics-quality' not in graphics:
        graphics['graphics-quality'] = "normal"
    if 'full-screen' not in graphics:
        graphics['full-screen'] = "false"
    if sys.platform.startswith('linux'):
        if 'force-opengl' not in graphics:
            graphics['force-opengl'] = "true"
        if 'video-memory-usage' not in graphics:
            graphics['video-memory-usage'] = "medium"
    with open(config_path, 'w') as cf:
        cf.write("; version=3\n")
        config.write(cf, space_around_delimiters=False)
        logging.debug(config)

    # mod symbolic link
    os.makedirs(os.path.dirname(mod_path), exist_ok=True)
    if 'force-symbolic-link' not in args and sys.platform == 'win32':
        # symbolic links require administrator rights in windows
        # so by default we use junctions
        # (but add an override option just in case)
        import _winapi
        _winapi.CreateJunction(path.abspath(directory), path.abspath(mod_path))
        logging.info("Junction created for %s → %s", directory, mod_path)
    else:
        os.symlink(path.abspath(directory), path.abspath(mod_path))
        logging.info("Symlink created for %s → %s", directory, mod_path)

    # run the game, showing log on console
    arguments = [
        path.join(factorio_path, 'bin', 'x64', 'factorio'), '-c', config_path,
        '--mod-directory',
        path.dirname(mod_path), '--enable-runtime-autoplace-modification'
    ]
    if verbose > 0:
        arguments.append('--verbose')
        logging.info("Factorio verbose logging on")
    if args['silent']:
        arguments.append('--disable-audio')
        logging.info("Factorio audio off")
    logging.debug("Factorio arguments: %s", arguments)
    print("Running {1}Factorio {3}{0} for {2}{4} v{5}".format(
        Fore.RESET, Fore.YELLOW, Fore.CYAN, factorio_info['version'],
        info['name'], info['version']))
    subprocess.run(arguments)


def abort():
    logging.warning("Keyboard interrupt")
    pass
