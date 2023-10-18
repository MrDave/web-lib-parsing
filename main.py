import requests
from environs import Env
from pathlib import Path


def download_book(path, book_id):
    url = "https://tululu.org/txt.php"
    params = {
        "id": book_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    with open(path, "wb") as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history and response.url == "https://tululu.org/":
        raise requests.HTTPError


def main():
    env = Env()
    env.read_env()

    media_folder = env.str("MEDIA_FOLDER")
    Path(media_folder).mkdir(exist_ok=True, parents=True)

    for book_id in range(1, 11):
        path = Path(media_folder).joinpath(f"book_{book_id}.txt")
        try:
            download_book(path, book_id)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
