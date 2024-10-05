#!/usr/bin/env python3

# %%
from bs4 import BeautifulSoup
import requests
import re


# %%
class Scraper:
    def __init__(self):
        pass

    def __call__(self, url, print_scarps=False):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        strips = list(soup.stripped_strings)
        print("url:", url)
        if print_scarps:
            print("strips:", strips)
        print("email:", self.get_email(strips))
        print("zip and country:", self.get_zip_and_country(strips))
        print("phone:", self.get_phone_number(strips))

    def get_email(self, strips):
        email_regex = r"[\w.+-]+@[\w-]+\.[\w.-]+"
        r = re.compile(email_regex)
        return list(filter(r.match, strips))

    def get_zip_and_country(self, strips):
        zip_regex = r"\d{5}( \d|$)"
        r = re.compile(zip_regex)
        return list(filter(r.match, strips))

    def get_phone_number(self, strips):
        phone_regex = r"^(\+|\d).+"
        for i, a in enumerate(strips):
            if "telefon" in a.lower() or "nummer" in a.lower():
                first_string = re.sub(r"^.*? ", "", a)
                match1 = re.search(phone_regex, first_string)
                match2 = re.search(phone_regex, strips[i + 1])
                if match1 is not None or match2 is not None:
                    return match1.group(0) if match2 is None else match2.group(0)


# %%
with open("urls.txt") as f:
    urls = f.readlines()
urls = list(filter(lambda s: s[0:4].lower() == "http", map(lambda s: s.strip(), urls)))

# %%
scraper = Scraper()
for url in urls:
    write_strips = False
    # url4 = "https://www.htw-berlin.de/impressum/"
    # if url == url4: # chnage the url to show the list of elements
    #     write_strips = False # change True to show list
    scraper(url, write_strips)
