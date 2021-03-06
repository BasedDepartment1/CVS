import sys
import time
import logging


# All functions are just for the sake of demonstration how main() will work
def init(*args):
    print("init cool")


def add(*args):
    if len(args) != 1:
        logging.error("Incorrect format: number of arguments must be 1 "
                      + f"but was: {len(args)}")
        sys.exit(2)

    print("adding...")
    time.sleep(1)


def commit(*args):
    if len(args) == 2 and args[0] == "-m":
        print(args[1])
    elif args == ([],):
        print("commit no message")
    else:
        logging.error("Number of arguments must be 2 or 0 "
                      + f"but was: {len(args)}")
        sys.exit(3)


def reset(*args):
    print("reset")


def log(*args):
    print("1: ya")
    print("2: ebal")
    print("3: sobaky")


COMMANDS = {
    "init": init,
    "add": add,
    "commit": commit,
    "reset": reset,
    "log": log,
}


def main():
    fmt = "[%(levelname)s] %(message)s"
    logging.basicConfig(format=fmt, level=logging.ERROR)

    if len(sys.argv) == 1:
        logging.error("No args")
        sys.exit(1)

    try:
        COMMANDS[sys.argv[1]](*sys.argv[2:])
    except KeyError:
        logging.error("No such command")
        sys.exit(4)


if __name__ == '__main__':
    main()
