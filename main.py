import os
import time
from random import random

import requests
from datetime import date

import schedule as schedule

from hackernews import HackernewsWrapper

non_url_safe = ['"', '#', '$', '%', '&', '+',
                ',', '/', ':', ';', '=', '?',
                '@', '[', '\\', ']', '^', '`',
                '{', '|', '}', '~', "'", '’']

hackernews = HackernewsWrapper()


def write_new_readme():
    item_dict = hackernews.get_top_item()
    title = item_dict.get("title")
    url = item_dict.get("url")
    text = create_rst_file(title, url)
    today = date.today().strftime("%Y-%m-%d")

    with open("archive/" + today + "--" + slugify(title) + ".rst", "w") as f:
        f.write(text)
    with open("README.rst", "w") as f:
        f.write(text)

    os.system('git add archive/*')
    os.system('git add README.rst')
    os.system("git commit -m '" + title + "'")
    os.system("git push origin")


def create_rst_file(title, url):
    underline = "".join(["=" * len(title)])
    linebreak = "\n"
    text = title + linebreak + underline + linebreak + "Here is the link of this story:" + linebreak + url
    return text


def slugify(text):
    non_safe = [c for c in text if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            slug = text.replace(c, '')
    text = u'_'.join(text.split())
    return text


schedule.every().day().at("10:30").do(write_new_readme)

while True:
    schedule.run_pending()
    time.sleep(3600)
