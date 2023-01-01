import requests
from bs4 import BeautifulSoup
import re

class WebtoonParser():
    def __init__(self, url, current):
        self.name = "Webtoon Parser"
        self.url = url
        self.current = current
        self.last = 0
        self.results = []
        self.pages = []
        self.runUpdate()

    def runUpdate(self):
        if self.current == '':
            print("recurse")
            self.get_all_pages(self.url)

        else:
            print("one page")
            self.search(self.url)
            if self.current not in self.results:
                print('not found in first page, recurse')
                self.get_all_pages(self.url)

        

    def get_all_pages(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
         
        self.search(url)
        if len(self.pages) == 0:
            result = soup.find_all('div', {'class': 'paginate'})
            for res in result:
                pages = re.findall(r'<span>(\d)<\/span>', str(res))
                for i in pages:
                    new_url = url + f"&page={i}"
                    self.search(new_url)
                    if self.current in self.results:
                        break
                

    def search(self, url):
        req = requests.get(url)
        page = req.content
        soup = BeautifulSoup(page, features="html.parser")
        res = soup.find_all('span', {'class': 'subj'})
        for i in res:
            self.results.append(i.get_text())
