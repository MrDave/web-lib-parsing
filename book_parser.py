import requests
from environs import Env
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, is_valid_filename
from urllib import parse
from argparse import ArgumentParser
from time import sleep
import logging
import functools


def retry_on_failure(max_retries=5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for retry_attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(f"Failed to execute {func.__name__}. Retrying in {4 ** retry_attempt}s. Error: {e}")
                    sleep(4 ** retry_attempt)
            logging.error(f"Failed to execute {func.__name__} after {max_retries} attempts.")
        return wrapper
    return decorator


@retry_on_failure(exceptions=(requests.ConnectionError, requests.Timeout))
def download_txt(url, filename, media_folder):
    """Download text files.

    Args:
        url (str): url of a file to download.
        filename (str): file name to save the file as (without ".txt" extension).
        media_folder (str): folder to save the file to.

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


@retry_on_failure(exceptions=(requests.ConnectionError, requests.Timeout))
def fetch_book_page(book_id: int):
    url = f"http://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def parse_book_page(response, book_id: int):
    """Parse book webpage for book info, comments and download/cover links."""

    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("body").find("h1")
    book_title = title_tag.text.split("::")[0].strip()
    book_author = title_tag.find("a").text
    book_link = f"https://tululu.org/txt.php?id={book_id}"

    image_tag = soup.find(class_="bookimage").find("img")
    image_link = f"https://tululu.org{image_tag["src"]}"

    comment_tags = soup.find_all(class_="texts")
    comments = [tag.find("span").text for tag in comment_tags]

    genre_tags = soup.find("span", class_="d_book").find_all("a")
    genres = [tag.text for tag in genre_tags]

    return book_title, book_author, book_link, image_link, comments, genres


@retry_on_failure(exceptions=(requests.ConnectionError, requests.Timeout))
def download_image(image_link, image_folder):
    """Download image from url link

    Args:
        image_link (str): url link to an image.
        image_folder (str): folder to save the image to.

    Returns:
        str: filepath of the saved image.
    """
    parsed_link = parse.urlsplit(image_link)
    image_name = parse.unquote(parsed_link.path.split("/")[-1])
    if not is_valid_filename(image_name):
        image_name = sanitize_filename(image_name)

    response = requests.get(image_link)
    response.raise_for_status()
    path = Path(image_folder).joinpath(image_name)
    with open(path, "wb") as file:
        file.write(response.content)

    return path


def main():
    env = Env()
    env.read_env()

    parser = ArgumentParser(
        description="Download books from tululu.org website in .txt format. Book IDs start at \"1\"."
    )
    parser.add_argument("start_id", type=int, help="ID of the first book to download")
    parser.add_argument("end_id", type=int, help="ID of the last book to download")

    args = parser.parse_args()

    book_folder = env.str("BOOK_FOLDER", default="books")
    image_folder = env.str("IMAGE_FOLDER", default="images")
    Path(book_folder).mkdir(exist_ok=True, parents=True)
    Path(image_folder).mkdir(exist_ok=True, parents=True)

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_page = fetch_book_page(book_id)
            title, author, book_link, image_link, comments, genres = parse_book_page(book_page, book_id)
            filename = f"{book_id}. {title}"
            download_txt(book_link, filename, book_folder)
            download_image(image_link, image_folder)
            print(
                f"Title: {title}\n"
                f"Author: {author}\n"
                f"Genre(s): {genres}\n"
            )
            if comments:
                print("Comment(s):")
                for comment in comments:
                    print(f"> {comment}\n")
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
