import sys
from pathlib import Path
from argparse import ArgumentParser

import niquests
from loguru import logger as log

def get_id(url: str) -> str:
    """
    Take a tver.jp url and extract the episode id
    Return the id only
    """
    split_url = url.rsplit("/", 1)
    log.debug(split_url)

    episode_id = split_url[-1]
    log.info("Id found: {}", episode_id)

    return episode_id


def main():
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("-json", action="store_true")
    parser.add_argument("-debug", action="store_true")
    args = parser.parse_args()

    if not args.debug:
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        log.remove()
        log.add(sys.stderr, level="INFO", format=fmt)

    episode_id = get_id(args.url)

    return 0


if __name__ == "__main__":
    main()
