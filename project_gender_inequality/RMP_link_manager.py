#!/usr/bin/env python

def read_by_lines(filename):
	"""
	Take a file and return an iterator object containing each line including nextline
	"""
	with open(filename) as f:
		content = f.readlines()
	for line in content:
		yield line[:-1]

def scrape_prof_info(prof_url):
	"""
	Takes the URL of the professor and returns a soup object of source
	"""
	from scrapy import scrape_url
	from time import sleep
	from urllib2 import URLError
	try:
		return scrape_url('http://' + prof_url)
	except:
		print 'Something wrong. Retrying: http://' + prof_url
		sleep(1)
		try:
			return scrape_url('http://' + prof_url)
		except:
			raise URLError('Could not find source. Skipping: http://' + prof_url)

def reduce_to_rpanel(prof_soup):
	"""
	Takes the source soup and returns only the soup with right panel
	"""
	try:
		return prof_soup.find('div', {'class': 'right-panel'})
	except:
		print 'Something wrong. Could not find right-panel.'
		raise

#if __name__ == '__main__':
#	main()