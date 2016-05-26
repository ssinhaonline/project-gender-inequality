#!/usr/bin/env python
if __name__ == '__main__':
	from scrapy import scrape_url
	from pdb import set_trace
	from time import sleep
	#set_trace()
	with open('RMP_prof_urls.txt', 'a') as f:
		for offset in range(940040, 1000000, 20):
			#try:
			url = 'http://www.ratemyprofessors.com/search.jsp?query=*&queryoption=HEADER&stateselect=&country=&dept=&queryBy=&facetSearch=&schoolName=&offset=' + str(offset) + '&max=20'
			try:
				src_soup = scrape_url(url)
			except:
				print 'Could not find: ' + url
				with open('RMP_prof_urls.log', 'a') as logger:
					logger.write('Could not find: ' + url + '\n')
				logger.close()
			try:
				listings = src_soup.find('ul', {'class': 'listings'})
			except:
				print "No Listings at: " + url
				with open('RMP_prof_urls.log', 'a') as logger:
					logger.write("No Listings at: " + url + '\n')
				logger.close()
			try:
				for listing in listings.find_all('li', {'class': 'listing PROFESSOR'}):
					try:
						f.write('www.ratemyprofessors.com' + listing.a['href'] + '\n')
						print 'Written :' + 'www.ratemyprofessors.com' + listing.a['href']
					except:
						print 'Could not write to file.'
						with open('RMP_prof_urls.log', 'a') as logger:
							logger.write('Could not write to file. URL: ' + url + '\n')
						logger.close()
			except:
				with open('RMP_prof_urls.log', 'a') as logger:
					logger.write('find_all crashed at: ' + url + '\n')
				logger.close()
			#except:
				#print url
