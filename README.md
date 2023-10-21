# [tululu.org](https://tululu.org/) book parser
Parse books' webpages and download them in `.txt` extension.
 
## How to install

Python should already be installed.

Use of virtual environment such as [venv](https://docs.python.org/3/library/venv.html) is recommended. 

Download the project files, install requirements using `pip` (or `pip3` if there is a conflict with Python2).
```commandline
pip install -r requirements.txt
```

To set custom download path for book and their cover images write the following settings to `.env` file in root folder of the project:
```
BOOK_FOLDER = # path to the desired place to save books 
IMAGE_FOLDER = # path to the desired place to save books' covers
```

## How to use

To use the script run:
```commandline
python book_parser.py start_id end_id
```

The `start_id` and `end_id`are the first and the last book's ID to parse and download, respectively.

Example:
```commandline
$python book_parser.py 1 15
Title: Административные рынки СССР и России
Author: Кордонский Симон
Genre(s): ['Деловая литература']

Title: Азбука экономики
Author: Строуп Р
Genre(s): ['Деловая литература']

...

Title: Бархатная революция в рекламе
Author: Зимен Сержио
Genre(s): ['Деловая литература']

Comment(s):

>Книга для настоящий рекламщиков!

>Это просто история жизни одного рекламщика. А где он "предланает свой революционный взгляд" так и не понятно!

>Очень познавательная книга, расскрывающая глаза на многие вещи.

>Интересная книга.

>Все вокруг да около! Ни слова о сути!

...
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
