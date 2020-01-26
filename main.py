import os
import time
from datetime import date
from random import randrange

import schedule as schedule

from contributionsmap import ContributionsMap
from hackernews import HackernewsWrapper

DAILY_TASKS_TAG = 'daily-tasks'

NON_URL_SAFE_CHARS = ['"', '#', '$', '%', '&', '+',
                      ',', '/', ':', ';', '=', '?',
                      '@', '[', '\\', ']', '^', '`',
                      '{', '|', '}', '~', "'", '’']

contributionsmap = ContributionsMap()
hackernews = HackernewsWrapper()


def write_pixel():
    print("running daily job")
    count = contributionsmap.get_count_by_date(date.today())
    print("write a pixel with value " + str(count))
    print("get the list of top news items")
    id_list = hackernews.get_top_items()

    for i in range(count):
        print("write item number " + str(i) + " of " + str(count) + " items")
        item_dict = hackernews.get_item(id_list[count - i - 1])
        write_new_readme(item_dict)
        time.sleep(randrange(0, 3600))


def write_new_readme(item_dict):
    title = item_dict.get("title")
    url = item_dict.get("url")
    print("inspecting item with title " + title + " and URL " + url)
    print("creating rst file")
    text = create_rst_file(title, url)
    today = date.today().strftime("%Y-%m-%d")

    print("copying the new item to the archive")
    with open("archive/" + today + "--" + slugify(title) + ".rst", "w") as f:
        f.write(text)
    print("write the new readme")
    with open("README.rst", "w") as f:
        f.write(text)

    print("commit changes to github")
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
    non_safe = [c for c in text if c in NON_URL_SAFE_CHARS]
    if non_safe:
        for c in non_safe:
            slug = text.replace(c, '')
    text = u'_'.join(text.split())
    return text

print("scheduling the write pixel task every day at 10:30 utc")
schedule.every().day.at('10:30').do(write_pixel)

while True:
    schedule.run_pending()
    time.sleep(3600)
