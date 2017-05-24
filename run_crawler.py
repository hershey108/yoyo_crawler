import sys
from yoyo_crawler import YoyoCrawler

# Confirm we have enough parameters for our script (assuming we're invoking it by explicitly calling python)
if len(sys.argv) < 2:
    print('Please provide a url to crawl')
    sys.exit()

crawler = YoyoCrawler(sys.argv[1].lower())
crawler.process_crawler()

# If we don't have any links or assets, it's
if len(crawler.links) == 0 and len(crawler.assets) == 0:
    print('No sitemap for ') + crawler.url
    sys.exit()

# Print a listing of the pages on the site
print('Sitemap:')
for path in crawler.sitemap.keys():
    print(path)
print('\n')

# Print the assets referenced on each page
for path in crawler.sitemap.keys():
    if len(crawler.sitemap[path]) > 0:
        print("Assets for " + path)
        for asset in crawler.sitemap[path]:
            print(asset)
        print('\n')
