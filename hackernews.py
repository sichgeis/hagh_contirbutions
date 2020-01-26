import requests


class HackernewsWrapper:
    url = "https://hacker-news.firebaseio.com/"

    def get_top_items(self):
        top_list = requests.get(self.url + "v0/topstories.json")
        return top_list.json()

    def get_item(self, id):
        s = self.url + "v0/item/" + str(id) + ".json"
        item = requests.get(s)
        item_dict = item.json()
        return item_dict

    def get_top_item(self):
        return self.get_item(self.get_top_item()[0])
