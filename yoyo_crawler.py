from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urlparse

class YoyoCrawler:

    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.path = urlparse(url).path
        self.links = set()
        self.assets = set()
        self.soup = self.getSoup()


    def getSoup(self):
        html = urlopen(self.url)
        return BeautifulSoup(html, 'html.parser')

    def getLinks(self):
        for link in self.soup.find_all('a'):
            if urlparse(link).netloc == self.domain:
                self.links.add(link)

    def getAssets(self):
        for asset in self.soup.find_all(['link','script','img']):
            if asset['href']:
                self.assets.add(asset['href'])
            elif asset['src']:
                self.assets.add(asset['src'])