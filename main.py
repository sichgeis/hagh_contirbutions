import os
import time

import requests
from datetime import date

import schedule as schedule

non_url_safe = ['"', '#', '$', '%', '&', '+',
                ',', '/', ':', ';', '=', '?',
                '@', '[', '\\', ']', '^', '`',
                '{', '|', '}', '~', "'", '’']


def get_top_item_id():
    top_list = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    return top_list.json()[0]


def get_item(id):
    s = "https://hacker-news.firebaseio.com/v0/item/" + str(id) + ".json"
    item = requests.get(s)
    item_dict = item.json()
    return item_dict


def create_rst_file(title, url):
    underline = "".join(["=" * len(title)])
    linebreak = "\n"
    text = title + linebreak + underline + linebreak + "Here is the link of this story:" + linebreak + url
    return text


def write_new_readme():
    item_dict = get_item(get_top_item_id())
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


def slugify(text):
    non_safe = [c for c in text if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            slug = text.replace(c, '')
    text = u'_'.join(text.split())
    return text


schedule.every(7).hours.do(write_new_readme)

while True:
    schedule.run_pending()
    time.sleep(3600)
