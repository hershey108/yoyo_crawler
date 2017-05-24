from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urlparse


class YoyoCrawler:
    """A web crawler that will parse a website, and provide a sitemap and list of assets for each page of the site that
    are reachable via a web of links from the homepage. 
    
    """

    def __init__(self, url, sitemap={}):
        self.sitemap = sitemap
        self.url = url
        self.scheme = urlparse(url).scheme
        self.domain = urlparse(url).netloc
        self.path = urlparse(url).path
        self.links = set()
        self.assets = set()
        self.soup = self.get_soup()

    def get_soup(self):
        """
        Attempt to get a webpage and return the BeautifulSoup object for it.
        """
        try:
            html = urlopen(self.url)
            return BeautifulSoup(html, 'html.parser')
        except:
            return None

    def get_links(self):
        """
        Searches the current page for all the links on it to other pages within the site, and updates the instance with
        that set. Also updates the sitemap reference so the originating script can access it.
        """
        for link in self.soup.find_all('a'):
            if 'href' in link.attrs:
                href = link['href'].lower()
                if href.startswith('/'):
                    href = self.scheme + '//' + self.domain + href
                elif ':' not in href:
                    href = self.scheme + '://' + self.domain + '/' + href

                if urlparse(href).netloc == self.domain and urlparse(href).path not in self.sitemap.keys():
                    self.links.add(href)
                    self.sitemap[urlparse(href).path] = set()

    def get_assets(self):
        """
        Tracks the images, CSS stylesheets and scripts that are referenced in the page.
        """
        for asset in self.soup.find_all(['link', 'script', 'img']):
            if 'href' in asset.attrs:
                self.assets.add(asset['href'])
            elif 'src' in asset.attrs:
                self.assets.add(asset['src'])

    def process_crawler(self):
        """
        Runs the process of getting the links and assets for a page, and recursively calling the crawler on sub-pages as
         necessary. 
        """
        if self.soup is None:
            return
        # Don't forget to add yourself to the sitemap if you're not on there already - useful for sites that never link
        #  back to the homepage
        if self.path not in self.sitemap.keys():
            self.sitemap[self.path] = set()
        self.get_assets()
        self.get_links()
        if len(self.links) > 0:
            for link in self.links:
                linkcrawler = YoyoCrawler(link,self.sitemap)
                linkcrawler.process_crawler()
                self.sitemap[linkcrawler.path] = linkcrawler.assets
