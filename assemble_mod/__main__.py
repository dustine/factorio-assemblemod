import sys
import traceback
import logging
from time import sleep
import argparse
from assemble_mod import assembler

PARSER = argparse.ArgumentParser(fromfile_prefix_chars='@')
PARSER.add_argument('directory', metavar='mod', help='mod directory')
PARSER.add_argument(
    '-v',
    '--verbose',
    action='count',
    default=0,
    help='log verbosity (-vv for script too)')
execution = PARSER.add_mutually_exclusive_group()
execution.add_argument(
    '--deploy', action='store_true', help='makes zip from HEAD (needs git)')
execution.add_argument(
    '-m',
    '--multiplayer',
    action='count',
    default=0,
    help='starts server test (-mmm... = m user instances)')
PARSER.add_argument(
    '-s',
    '--silent',
    action='store_true',
    help='disables game audio (faster load specially ≤ 0.15)')
PARSER.add_argument(
    '-r',
    '--reset',
    action='count',
    help="""clears the mod cache,
    -r resets config, 
    -rr erases mod loadout,
    -rrr resets *everything*""")


def run():
    # Argv Parser
    args = PARSER.parse_args()
    if args.verbose > 2:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose > 1:
        logging.basicConfig(level=logging.INFO)
    logging.info("Arguments passed: %s", vars(args))

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
