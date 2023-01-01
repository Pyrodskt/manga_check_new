import json
import threading
from JapscansParser import JapscansParser
from WebtoonParser import WebtoonParser
from MangarockteamParser import MangarockteamParser

class Mangas:
    def __init__(self, window):
        self.window = window
        self.mangas = []        
        self.updated = False
        self.update_progress = 0
        self.datas = self.read_file()
        self.createMangas()


    def write_file(self):

        content = {
            "datas": []
        }
        for i in self.mangas:
            content['datas'].append({'title': i.title, 'url': i.url, 'list': i.results, "current": i.current})

        with open("data.json", "w") as fichier:
            fichier.write(json.dumps(content))
        
    def read_file(self):
        with open("data.json", "r") as fichier:
            content = json.loads(fichier.read())
        return content

    def createMangas(self):
        for i in self.datas['datas']:
            self.mangas.append(Manga(i['title'], i['url'], i['list'], i['current']))

    def updateMangas(self):
        for i in self.mangas:
            i.start()
        self.updated = True
            



class Manga(threading.Thread):
    def __init__(self, title, url, list, current):
        threading.Thread.__init__(self)
        self.title = title 
        self.url = url
        self.current = current
        self.list = list
        self.parser = None
        self.last = ""
        self.results = []

    def run(self):

        if 'japscan' in self.url:
            self.parser = JapscansParser(self.url, self.current)

        if 'webtoons' in self.url:
            self.parser = WebtoonParser(self.url, self.current)

        if 'mangarockteam' in self.url:
            self.parser = MangarockteamParser(self.url, self.current)

        self.results = self.parser.results
        self.last = self.results[0]

    def update_current(self, new):
        self.current = new
 