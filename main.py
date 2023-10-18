import requests
from environs import Env
from pathlib import Path


def download_file(path, url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)


def main():
    env = Env()
    env.read_env()

    media_folder = env.str("MEDIA_FOLDER")
    Path(media_folder).mkdir(exist_ok=True, parents=True)
    book_link = "https://tululu.org/txt.php?id=32168"
    path = Path(media_folder).joinpath("Пески Марса.txt")

    download_file(path, book_link)


if __name__ == '__main__':
    main()
