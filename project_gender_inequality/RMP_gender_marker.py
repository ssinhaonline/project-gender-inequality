#!/usr/bin/env python

import RMP_mongo as Rmon
from nltk.tokenize import word_tokenize
from nltk import download
from pymongo import MongoClient

download('punkt')

def determine_gender(comment_list):
	"""
	Takes a list of all comment text received by professor and determines
	gender of professor depending on the frequncy of gender specific pronouns like
	'he', 'him', 'his', 'man', 'guy', 'male' versus 'she', 'her', 'hers', 'woman', 'lady' etc.
	Source: https://en.wikipedia.org/wiki/Gender-specific_and_gender-neutral_pronouns
	Returns either 'M' or 'F'
	"""
	gen_dict = {'M': 0, 'F': 0}
	for comment in comment_list:
		comment_tokens = word_tokenize(comment)
		comment_tokens = [token.lower() for token in comment_tokens]
		
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('he')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('him')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('his')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('man')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('guy')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('male')
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count("he's")
		gen_dict['M'] = gen_dict['M'] + comment_tokens.count('himself')
		
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('she')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('her')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('hers')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('herself')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('woman')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('lady')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('female')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count('herself')
		gen_dict['F'] = gen_dict['F'] + comment_tokens.count("her's")

	#print 'M: ' + str(gen_dict['M']) + ', F: ' + str(gen_dict['F'])
	if(gen_dict['M'] > gen_dict['F']):
		return 'M'
	if(gen_dict['F'] > gen_dict['M']):
		return 'F'
	if(gen_dict['F'] == gen_dict['M']):
		return 'U'

def marker():
	"""
	This function takes each record from the mongoDB rmpdb database
	and updates it as 'M' or 'F' as determined by determine_gender() function above.
	"""
	#from pdb import set_trace
	#set_trace()
	client = MongoClient()
	rmpdb = client['rmpdb']
	profs = rmpdb['profs']
	cursor = profs.find(dict(), {'all comments.rComments': 1})
	for record in cursor:
		Objid = record['_id']
		comments = list()
		[comments.append(comment['rComments']) for comment in record['all comments']]
		gender = determine_gender(comments)
		profs.update({'_id': Objid}, {'$set': {"gender": gender}})
		print profs.find_one({"_id" : Objid}, {"name": 1, "gender" : 1})

def find_unidentified():
	profs = MongoClient()['rmpdb']['profs']
	cursor = profs.find({'gender': 'U'})
	unidentified_records = list()
	[unidentified_records.append(record) for record in cursor]
	return unidentified_records

if __name__ == '__main__':
	marker()



