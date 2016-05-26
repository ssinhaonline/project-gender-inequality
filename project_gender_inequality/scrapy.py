#!/usr/bin/env python
"""
This module is meant to be used for scraping websites.
"""
def scrape_url(url):
	"""
	Take the parameter url and return a BeautifulSoup tree
	"""
	from urllib2 import urlopen
	from bs4 import BeautifulSoup
	
	src = urlopen(url)

	return BeautifulSoup(src, 'html.parser')

