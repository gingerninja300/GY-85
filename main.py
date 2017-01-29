import argparse

from main_client import start_loop_client
from main_server import start_loop_server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("server", type=int, help="if the app should be the server (1) or client (0)")
    parser.add_argument("--stdout", help="write to stdout instead of file", action="store_true")
    parser.add_argument("-nth", type=int, help="only print ever nth sample if --stdout is specified")
    args = parser.parse_args()

    if args.server:
        start_loop_server(args)
    else:
        start_loop_client(args)
