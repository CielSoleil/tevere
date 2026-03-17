import sys
from pathlib import Path
from argparse import ArgumentParser

import niquests
from loguru import logger as log

def main():
    parser = ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-debug", action="store_true")
    args = parser.parse_args()

    if not args.debug:
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        log.remove()
        log.add(sys.stderr, level="INFO", format=fmt)

    return 0


if __name__ == "__main__":
    main()
