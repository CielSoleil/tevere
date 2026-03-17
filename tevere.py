import sys
from pathlib import Path
from argparse import ArgumentParser

import niquests
from loguru import logger as log

def main():
    parser = ArgumentParser()
    parser.add_argument("-debug", action="store_true")
    args = parser.parse_args()

    return 0


if __name__ == "__main__":
    main()
