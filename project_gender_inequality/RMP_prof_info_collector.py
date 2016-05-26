#!/usr/bin/env python

def get_prof_id(prof_url):
	"""
	Takes the URL and returns the ID of the professor
	"""
	parts = prof_url.split('=')
	return parts[1]

def get_prof_name(rpan_soup):
	"""
	Take right-panel soup and return the name, ignore middle name
	"""
	try:
		name_soup = rpan_soup.find('h1', {'class': 'profname'})
		unclean_firstname = name_soup.find('span', {'class': 'pfname'}).string
		firstname = ''.join(unclean_firstname.split())	#Removing all whitespaces
		unclean_lastname = name_soup.find('span', {'class': 'plname'}).string
		lastname = ''.join(unclean_lastname.split())	#Removing all whitespaces
		return firstname + ' ' + lastname
	except:
		print 'Could not find name of Professor. Returning John Doe.'
		return 'John Doe'

def get_prof_details(rpan_soup):
	"""
	Take right-panel soup and return the dictionary of tag, university name, location
	"""
	#from pdb import set_trace
	try:
		#set_trace()
		tag_soup = rpan_soup.find('div', {'class': 'result-title'})
		tag_gen = tag_soup.stripped_strings
		#tagline = unclean_tagline.strip()
		stuff = list()
		for item in tag_gen:
			stuff.append(item)
		city_state = stuff[3].split(',')
		city_state[1] = city_state[1].strip()
		city_state[2] = city_state[2].strip()
		return {"tag": stuff[0], 
				"university": stuff[2], 
				"city": city_state[1], 
				"state": city_state[2]}
	except:
		print "Did not find details. Returning empty strings."
		return {"tag": '', 
				"university": '', 
				"city": '', 
				"state": ''}

def get_prof_ratings(rpan_soup):
	"""
	Take right-panel soup and return the dictionary of ratings
	"""
	try:
		rat_pan = rpan_soup.find('div', {'class', 'left-breakdown'})
		header_soups = rat_pan.find_all('div', {'class', 'breakdown-header'})
		ovr = header_soups[0].find('div', {'class', 'grade'}).string
		avg_grade = header_soups[1].find('div', {'class', 'grade'}).string
		rat_slide = rat_pan.find('div', {'class', 'faux-slides'})
		sliders = rat_slide.find_all('div', {'class', 'rating-slider'})
		hlpfl = sliders[0].find('div', {'class', 'rating'}).string
		clrt = sliders[1].find('div', {'class', 'rating'}).string
		easiness = sliders[2].find('div', {'class', 'rating'}).string
		return {"overall-quality": ovr,
				"avg-grade-received": avg_grade,
				"helpfulness": hlpfl, 
				"clarity": clrt,
				"easiness": easiness}
	except:
		print 'Could not copy ratings. Returning empty dictionary'
		return {"overall-quality": '',
				"avg-grade-received": '',
				"helpfulness": '', 
				"clarity": '',
				"easiness": ''}

def get_top_tags(rpan_soup):
	"""
	Take right-panel soup and return the top tags of the professor (max 20)
	"""
	#from pdb import set_trace
	#from re import search
	try:
		#set_trace()
		tagbox_soup = rpan_soup.find('div', {'class', 'tag-box'})
		tags_soup = tagbox_soup.find_all('span', {'class', 'tag-box-choosetags'})
		tags = []
		for tag in tags_soup:
			tag_strings = tag.stripped_strings
			tag_elms = []
			for s in tag_strings:
				tag_elms.append(s)
			tag_dict = {}
			tag_dict['tag-name'] = tag_elms[0]
			score = tag_elms[1]
			tag_dict['tag-score'] = score[score.find('(') + 1 : score.find(')')]
			tags.append(tag_dict)
		return tags
	except:
		print "Could not collect tags. Returning empty list"
		return []


#if __name__ == '__main__':
#	main()