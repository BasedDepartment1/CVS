import sys
import time
import logging


def main():
    fmt = "[%(levelname)s] %(message)s"
    logging.basicConfig(format=fmt, level=logging.ERROR)

    if len(sys.argv) == 1:
        logging.error("No args")
        sys.exit(1)
    match sys.argv[1]:
        case "init":
            print("init cool")
        case "add":
            if len(sys.argv) == 2:
                logging.error("Nothing to add")
                sys.exit(2)
            print("adding...")
            time.sleep(5)
            sys.exit(0)
        case "commit":
            if len(sys.argv) == 4 and sys.argv[2] == "-m":
                print(sys.argv[3])
            else:
                print("commit no message")
        case "reset":
            print("reset")
        case "log":
            print("1: ya")
            print("2: ebal")
            print("3: sobaky")
        case _:
            logging.error("No such command")
            sys.exit(3)


if __name__ == '__main__':
    main()
