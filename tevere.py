import sys
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Any

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


def get_episode_data(api_response: dict[str, Any]) -> dict[str, Any]:
    """
    Take the api response we got from niquests.get()
    Return a dict with the only two relevant value: Series name, Episode title

    You can get more data out of this, but the script doesn't intend to use it.
    For now at least.
    """
    series = api_response.get("series")
    title = api_response.get("title")
    log.debug(series)
    log.debug(title)

    # Other values that can be obtained (commented out by default)
    # open_at = api_response.get("open_at")
    # close_at = api_response.get("close_at")
    # duration = api_response.get("duration")
    # index_number = api_response.get("index_number")

    # Series is another dict with the Series information, we just
    # want the title and only if we can access it
    # Give up if we can't get it
    if series == None:
        log.error("Series title can't be retrieved")
        raise ValueError
    
    series_title = series.get("title")

    return {"series" : series_title, "episode" : title}


def write_response_to_disk(api_response: dict[str, Any], 
                           episode_id: str, 
                           out_path: Path) -> None:
    """
    Take the JSON response and save it to disk.
    Save under the episode id as it goes easier on filename length and characters (decimal vs Japanse)
    The function itself doesn't return anything.
    """
    # It is assumed that we already checked and created the output path
    filename = f"{episode_id}.json"
    output = out_path / filename

    if output.exists():
        log.error("File {} exists", output)
        raise FileExistsError
    
    else:
        log.info("Saving to {}", output)

        with open(output, "w+") as o:
            log.info("Dumping API response now")
            json.dump(api_response, o, indent=4, ensure_ascii=False)
        o.close()



def main():
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("-json", action="store_true")
    parser.add_argument("-download", action="store_true")
    parser.add_argument("-dir", type=Path, default=Path("~/Videos/tver"))
    parser.add_argument("-debug", action="store_true")
    args = parser.parse_args()

    # Requests headers, do not modify unless you know what you're doing!
    h = {"user-agent" : "Mozilla/5.0",
         "x-tver-platform-type" : "web"}

    if not args.debug:
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        log.remove()
        log.add(sys.stderr, level="INFO", format=fmt)

    episode_id = get_id(args.url)
    episode_data_url = make_content_url(episode_id)

    # Request API
    log.info("GET {}", episode_data_url)
    r = niquests.get(episode_data_url, headers=h)
    response = r.json()

    # If we get a 404, give up
    if r.status_code == 404:
        log.error("Request failed: {}", r.status_code)
        log.error("API says: {}", response)
        raise ValueError
    
    # If the API response is empty, give up
    if response is None:
        log.error("JSON response is empty")
        raise ValueError
    
    log.debug(response)

    episode_data = get_episode_data(response)

    # This data will be used to create a better yt-dlp output template
    series = episode_data.get("series")
    episode = episode_data.get("episode")

    # Deal with ~
    main_dir = args.dir.expanduser()
    series_dir = main_dir / series

    # Report if directory doesn't exist
    if not series_dir.exists():
        log.info("Creating folder {}", series_dir)

    # But run mkdir() regardless
    series_dir.mkdir(parents=True, exist_ok=True)

    # Save data to disk (-json)
    if args.json:
        write_response_to_disk(response, episode_id, series_dir)



if __name__ == "__main__":
    main()
