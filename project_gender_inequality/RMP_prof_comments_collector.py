#!/usr/bin/env python

from urllib2 import urlopen

def get_prof_comments(prof_id):
	"""
	Take the professor's id and return a json object of all comments
	"""
	from json import load
	base_url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid='
	page_url = '&page='
	penult_url = base_url + prof_id + page_url
	paginator = 1
	try:
		ratings = load(urlopen(penult_url + str(paginator)))
		allratings = ratings['ratings']
		while not (ratings['remaining'] == 0):
			paginator += 1
			try:
				ratings = load(urlopen(penult_url + str(paginator)))
				allratings.extend(ratings['ratings'])
			except:
				continue
	except:
		allratings = []
	return allratings

def mongofy_comments():
	"""
	Take 'all comments' embedded documents from the 'profs' table and store
	them into another table 'comments' in 'rmpdb' database
	"""
	from pdb import set_trace
	set_trace()
	from pymongo import MongoClient
	profs_cur = MongoClient()['rmpdb']['profs'].find({},{'_id' : 1, 'gender': 1, 'all comments' : 1})
	db = MongoClient()['rmpdb']
	for prof in profs_cur:
		prof_id = str(prof['_id'])
		prof_gender = prof['gender']
		prof_comments = prof['all comments']
		for comment in prof_comments:
			comment['prof_id'] = prof_id
			comment['prof_gender'] = prof_gender
			try:
				date = comment['rDate']
				month, day, year = date.split('/')
			except:
				day = 1
				month = 1
				year = 1900
			comment['day'] = day
			comment['month'] = month
			comment['year'] = year
			result = db.comments.insert_one(comment)


#if __name__ == '__main__':
#	main()
		

		
