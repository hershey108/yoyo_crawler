# Overview
This is a python based web crawler that accepts a URL and then will follow all links on that and subsequent pages that
are on the same subdomain of the site. It will output a sitemap as a list of paths it has found, and a list of assets
for each page that has any linked in its source.
 
# Running
To run the script, simply call `python run_crawler.py <URL of SITE to crawl>`

# Future extension
This script does not take into account execution time, so it will run for a long time for large sites. It may be
preferable to cancel execution after a certain time or depth of links processed.
 
Also it would be possible to multi-thread the crawling when we have large sets of links to follow up on, though we risk
the potential of duplicating crawls due to race conditions when checking our current state of the sitemap.