import json

import requests

def get_top_item_id():
    top_list = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    return top_list.json()[0]

def get_item(id):
    s = "https://hacker-news.firebaseio.com/v0/item/" + str(id) + ".json"
    item = requests.get(s)
    item_dict = item.json()
    return item_dict

def create_rst_file(title, url):
    underline = "".join(["="*len(title)])
    linebreak = "\n"
    text = title + linebreak + underline + linebreak + "Here is the link of this story:" + linebreak + url
    return text

item_dict = get_item(get_top_item_id())
with open('README.rst', 'w') as f:
    f.write(create_rst_file(item_dict.get("title"), item_dict.get("url")))
    f.close()
