import sys
import traceback
# import os
from time import sleep
import argparse
from assemble_mod import assembler

PARSER = argparse.ArgumentParser(fromfile_prefix_chars='@')
PARSER.add_argument(
    'directory', metavar='mod', help='mod directory')
PARSER.add_argument(
    '-s',
    '--silent',
    action='store_true',
    help='disables game audio (faster load ≤ 0.15)')
PARSER.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='log verbosity (-vv for script too)')
deploy = PARSER.add_mutually_exclusive_group()
deploy.add_argument(
    '--deploy', action='store_true', help='makes zip from commit (needs git)')
deploy.add_argument(
    '-m',
    '--multiplayer',
    action='count',
    help='starts mp test (-mmm... = m users)')


def run():
    # Argv Parser
    args = PARSER.parse_args()

    try:
        assembler.run(**vars(args))
    except KeyboardInterrupt:
        assembler.abort()
        sleep(0.1)
        # tqdm.write("Shutdown requested... exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return 1


if __name__ == '__main__':
    run()
