import requests
from environs import Env
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, is_valid_filename


def download_txt(url, filename, media_folder):
    """Download text files.

    Args:
        url (str): url of a file to download.
        filename (str): file name to save the file as (without ".txt" extension).
        media_folder: folder to save the file to.

    Returns:
        str: filepath of the saved file.
    """
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    if not is_valid_filename(filename):
        filename = sanitize_filename(filename)

    path = Path(media_folder).joinpath(f"{filename}.txt")
    with open(path, "wb") as file:
        file.write(response.content)

    return path


def check_for_redirect(response):
    if response.history and response.url == "https://tululu.org/":
        raise requests.HTTPError


def parse_book_page(book_id: int):
    url = f"http://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("body").find("h1")
    book_title = title_tag.text.split("::")[0].strip()
    book_author = title_tag.find("a").text
    return book_title, book_author


def main():
    env = Env()
    env.read_env()

    media_folder = env.str("MEDIA_FOLDER", default="books")
    Path(media_folder).mkdir(exist_ok=True, parents=True)

    # for book_id in range(1, 11):
    #     path = Path(media_folder).joinpath(f"book_{book_id}.txt")
    #     try:
    #         download_book(path, book_id)
    #     except requests.HTTPError:
    #         continue
    title, author = parse_book_page(1)
    print(f"Название: {title}\nАвтор: {author}")


if __name__ == '__main__':
    main()
