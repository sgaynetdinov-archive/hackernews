from urllib.request import urlopen

from parsel import Selector

URL = 'https://news.ycombinator.com/'


class HackerNewsParser:
    _html = None

    def download(self):
        response = urlopen(URL)
        self._html = response.read()

    def as_json(self):
        sel = Selector(text=self._html)

        data = []

        for tr in sel.css('.athing'):
            data.append({
                "hacker_news_id": tr.attrib['id'],
                "url": tr.css('.storylink').attrib['href'],
                "title": tr.css('.storylink::text').get()
            })

        return data
