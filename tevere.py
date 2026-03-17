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


def make_content_url(episode_id: str) -> str:
    """
    Take the episode id returned by get_id()
    Return an API url for TVer
    """
    content_api = f"https://contents-api.tver.jp/contents/api/v1/episodes/{episode_id}"
    log.debug(content_api)

    return content_api


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
    episode_data_url = make_content_url(episode_id)

    return 0


if __name__ == "__main__":
    main()
