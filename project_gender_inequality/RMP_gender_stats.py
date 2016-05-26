#!/usr/bin/env python

from pymongo import MongoClient
from csv import DictWriter
from random import shuffle
from pdb import set_trace
from operator import itemgetter
from scipy.stats import pearsonr
from numpy import mean
from numpy import log2
from tqdm import tqdm
from re import sub

def get_ids_by_gender(profs_cur = MongoClient()['rmpdb']['profs'].find({}, {'_id' : 1, 'gender' : 1})):
	
	male_ids = list()
	female_ids = list()
	for rec in profs_cur:
		if rec['gender'] == 'M':
			male_ids.append(rec['_id'])
		if rec['gender'] == 'F':
			female_ids.append(rec['_id'])
	return (male_ids, female_ids)

def gendistr_ids_by_state(state = ''):
	"""

	"""
	#set_trace()
	if state == '':
		return get_ids_by_gender(profs_cur = MongoClient()['rmpdb']['profs'].find({}, {'_id' : 1, 'gender' : 1}))
	else:
		all_states = MongoClient()['rmpdb']['profs'].distinct('details.state')
		if state in all_states:
			cur = profs_cur = MongoClient()['rmpdb']['profs'].find({'details.state' : state}, {'_id' : 1, 'gender' : 1})
			return get_ids_by_gender(profs_cur = cur)
		else:
			print "Could not find state. Choose one of the following [choice]:"
			all_states.sort()
			for state in all_states:
				print state + ' [' + str(all_states.index(state)) + ']'
			try:
				state = all_states[int(raw_input('Enter [choice]: '))]
				return gendistr_ids_by_state(state)
			except:
				print "Sorry, couldn't find state!"
				return None

def gendistr_ids_by_department(department = ''):
	"""

	"""
	#set_trace()
	if department == '':
		return get_ids_by_gender(profs_cur = MongoClient()['rmpdb']['profs'].find({}, {'_id' : 1, 'gender' : 1}))
	else:
		all_depts = MongoClient()['rmpdb']['profs'].distinct('details.department')
		if department in all_depts:
			cur = profs_cur = MongoClient()['rmpdb']['profs'].find({'details.department' : department}, {'_id' : 1, 'gender' : 1})
			return get_ids_by_gender(profs_cur = cur)
		else:
			print "Could not find department. Choose one of the following [choice]:"
			all_depts.sort()
			for department in all_depts:
				print department + ' [' + str(all_depts.index(department)) + ']'
			try:
				department = all_depts[int(raw_input('Enter [choice]: '))]
				return gendistr_ids_by_department(department)
			except:
				print "Sorry, couldn't find department!"
				return None

def gendistr_ids_by_university(university = ''):
	"""

	"""
	#set_trace()
	if university == '':
		return get_ids_by_gender(profs_cur = MongoClient()['rmpdb']['profs'].find({}, {'_id' : 1, 'gender' : 1}))
	else:
		all_univs = MongoClient()['rmpdb']['profs'].distinct('details.university')
		if university in all_univs:
			cur = profs_cur = MongoClient()['rmpdb']['profs'].find({'details.university' : university}, {'_id' : 1, 'gender' : 1})
			return get_ids_by_gender(profs_cur = cur)
		else:
			print "Could not find university. Choose one of the following [choice]:"
			all_univs.sort()
			for university in all_univs:
				print university + ' [' + str(all_univs.index(university)) + ']'
			try:
				university = all_univs[int(raw_input('Enter [choice]: '))]
				return gendistr_ids_by_university(university)
			except:
				print "Sorry, couldn't find university!"
				return None

def get_rating_details(choice, grade = '', profs_collection = MongoClient()['rmpdb']['profs']):
	"""
	Enter choices exactly like 'Clarity', 'Helpful', 'Easy' for the distribution
	those features of students' comments. Rated as 1 - 5 ordinally.
	"""
	
	if grade == '':
		filename = '../fixtures/all_csv/' + choice + '_distribution.csv'
	else:
		filename = '../fixtures/all_csv/' + grade + '_' + choice + '_distribution.csv'
	with open(filename, 'w') as f:
		male_ids, female_ids = get_ids_by_gender()
		all_ids = male_ids + female_ids
		shuffle(all_ids)
		writer = DictWriter(f, fieldnames = ['id', choice + '_1', choice + '_2', choice + '_3', choice + '_4', choice + '_5', 'gender', 'num_comments'])
		writer.writeheader()
		for this_id in all_ids:
			if grade == '':
				prof = profs_collection.find_one({'_id' : this_id}, {'all comments': 1, 'gender': 1})
			else:
				prof = profs_collection.find_one({'_id' : this_id, 'all comments.teacherGrade' : grade}, {'all comments': 1, 'gender': 1})
				if prof == None:
					continue
				else:
					pass
			prof_id = str(prof['_id'])
			gender = prof['gender']
			choice_dict = {	'id' : prof_id,
							'gender': gender, 
							choice + '_1': 0,
							choice + '_2': 0,
							choice + '_3': 0,
							choice + '_4': 0,
							choice + '_5': 0,
							'num_comments': 0
						}
			grade_num_comments = 0
			for comment in prof['all comments']:
				
				if grade == '':
					pass	
				else:
					if comment['teacherGrade'] != grade:
						continue
					else:
						grade_num_comments += 1
						pass
				
				choice_score = comment['r' + choice]

				if choice_score == 1:
					choice_dict[choice + '_1'] += 1
				if choice_score == 2:
					choice_dict[choice + '_2'] += 1
				if choice_score == 3:
					choice_dict[choice + '_3'] += 1
				if choice_score == 4:
					choice_dict[choice + '_4'] += 1
				if choice_score == 5:
					choice_dict[choice + '_5'] += 1
			
			if grade == '':
				choice_dict['num_comments'] = len(prof['all comments'])
			else:
				choice_dict['num_comments'] = grade_num_comments

			writer.writerow(choice_dict)
	f.close()

def grade_dist_collector():
	"""

	"""
	grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D-', 'F', 'Drop', 'Incomplete', 'Not sure yet', 'Rather not say', 'Audit/No Grade', 'null']
	#grades = ['Audit_No Grade', 'null']
	ratings = ['Clarity', 'Helpful', 'Easy']

	for grade in grades:
		for rating in ratings:
			print 'Collecting : Rating - ' + rating + ' Grade - ' + grade
			get_rating_details(choice = rating, grade = grade)

def get_average_ratings_dist(profs_collection = MongoClient()['rmpdb']['profs']):
	
	filename = '../fixtures/all_csv/' + 'Avg_ratings_distribution.csv'
	
	with open(filename, 'w') as f:
		male_ids, female_ids = get_ids_by_gender()
		all_ids = male_ids + female_ids
		shuffle(all_ids)
		writer = DictWriter(f, fieldnames = ['id','avg-grade', 'clarity', 'easiness', 'helpfulness', 'overall-quality', 'city', 'state', 'university', 'department', 'gender'])
		writer.writeheader()
		
		for this_id in all_ids:

			avg_rat = dict()
			prof = profs_collection.find_one({'_id' : this_id, 'gender' : {'$in': ['M', 'F']}}, {'ratings' : 1, 'details' : 1, 'gender' : 1, '_id' : 1})
			
			avg_rat['id'] = str(prof['_id']).encode('utf-8')
			avg_rat['gender'] = prof['gender'].encode('utf-8')
			avg_rat['avg-grade'] = prof['ratings']['avg-grade-received'].encode('utf-8')
			avg_rat['clarity'] = prof['ratings']['clarity'].encode('utf-8')
			avg_rat['easiness'] = prof['ratings']['easiness'].encode('utf-8')
			avg_rat['helpfulness'] = prof['ratings']['helpfulness'].encode('utf-8')
			avg_rat['overall-quality'] = prof['ratings']['overall-quality'].encode('utf-8')
			avg_rat['city'] = prof['details']['city'].encode('utf-8')
			avg_rat['state'] = prof['details']['state'].encode('utf-8')
			avg_rat['university'] = prof['details']['university'].encode('utf-8')
			desc = prof['details']['tag']
			words = desc.split(' ')
			words = [word.lower() for word in words]
			initial = words.index('the')
			final = words.index('department')
			dept = u' '.join(words[initial + 1 : final])
			avg_rat['department'] = dept.encode('utf-8')

			writer.writerow(avg_rat)
	f.close()

def get_top_departments(switch, records = MongoClient()['rmpdb']['profs'].find({}, {'details': 1, '_id' : 1})):
	"""
	This function takes in the collection object and finds the get_top_departments
	department with 80 percent population of professors 
	"""
	
	#from pdb import set_trace
	#set_trace()
	#dept_set = record.distinct('details.department')
	dept_tab = dict()

	for record in records:
		if record['details']['department'] in dept_tab:
			dept_tab[record['details']['department']] += 1
		else:
			dept_tab[record['details']['department']] = 1
	if switch == 'P':
		eighty_div_total = int(records.count() * 0.8)
	if switch == 'D':
		eighty_div_total = int(len(dept_tab) * 0.8)

	sorted_dept_tab = sorted(dept_tab.items(), key = itemgetter(1), reverse = True)
	new_sort = []
	count = 0
	looper = 0
	while True:
		item = sorted_dept_tab[looper]
		if switch == 'P':
			count += item[1]
		if switch == 'D':
			count += 1
		new_sort.append(item)
		looper += 1
		if count > eighty_div_total:
			break

	return new_sort

def get_comment_rating_history_corr(switch = ''):
	from datetime import datetime
	set_trace()
	if switch == '':
		profs_cur = MongoClient()['rmpdb']['profs'].find({}, {'_id':1, 'all comments.rHelpful' : 1, 'all comments.rClarity' : 1, 'all comments.rEasy' : 1, 'all comments.rDate' : 1})
	else:
		if switch == 'M':
			profs_cur = MongoClient()['rmpdb']['profs'].find({'gender' : 'M'}, {'_id':1, 'all comments.rHelpful' : 1, 'all comments.rClarity' : 1, 'all comments.rEasy' : 1, 'all comments.rDate' : 1})
		elif switch == 'F':	
			profs_cur = MongoClient()['rmpdb']['profs'].find({'gender' : 'F'}, {'_id':1, 'all comments.rHelpful' : 1, 'all comments.rClarity' : 1, 'all comments.rEasy' : 1, 'all comments.rDate' : 1})
		else:
			ch = raw_input("Switch does not match, Select 'M', 'F' or leave blank: ")
			get_comment_rating_history_corr(switch = ch)

	help_dict = dict()
	clar_dict = dict()
	ease_dict = dict()

	zero_count = 0
	one_count = 0

	for prof in tqdm(profs_cur):
		comments = prof['all comments']
		if len(comments) == 0:
			zero_count += 1
			continue
		elif len(comments) == 1:
			one_count += 1
			#raw_input("1 comment here")
			if 1 not in help_dict:
				help_dict[1] = [[],[]]
			help_dict[1][0].append(float(comments[0]['rHelpful']))
			help_dict[1][1].append(float(comments[0]['rHelpful']))

			if 1 not in clar_dict:
				clar_dict[1] = [[],[]]
			clar_dict[1][0].append(float(comments[0]['rClarity']))
			clar_dict[1][1].append(float(comments[0]['rClarity']))
	
			if 1 not in ease_dict:
				ease_dict[1] = [[],[]]
			ease_dict[1][0].append(float(comments[0]['rEasy']))
			ease_dict[1][1].append(float(comments[0]['rEasy']))

		else:
			comments = sorted(comments, key = lambda x: datetime.strptime(x['rDate'], '%m/%d/%Y'))
			help_list = list()
			clar_list = list()
			ease_list = list()
			for comment in comments:
				help_list.append(float(comment['rHelpful']))
				clar_list.append(float(comment['rClarity']))
				ease_list.append(float(comment['rEasy']))
				
			for i in range(1, len(comments)):
				mean_n_minus_one_help = mean(help_list[0 : i])
				nth_help = help_list[i]
				if i not in help_dict:
					help_dict[i] = [[],[]]
				help_dict[i][0].append(mean_n_minus_one_help)
				help_dict[i][1].append(nth_help)

				mean_n_minus_one_clar = mean(clar_list[0 : i])
				nth_clar = clar_list[i]
				if i not in clar_dict:
					clar_dict[i] = [[],[]]
				clar_dict[i][0].append(mean_n_minus_one_clar)
				clar_dict[i][1].append(nth_clar)

				mean_n_minus_one_ease = mean(ease_list[0 : i])
				nth_ease = ease_list[i]
				if i not in ease_dict:
					ease_dict[i] = [[],[]]
				ease_dict[i][0].append(mean_n_minus_one_ease)
				ease_dict[i][1].append(nth_ease)

	with open('../fixtures/all_csv/Comment_history_correlation_Helpful' + switch + '.csv', 'w') as help_file:
		fieldnames = ['n', 'corr', 'p_val']
		help_writer = DictWriter(help_file, fieldnames = fieldnames)
		help_writer.writeheader()
		for key in help_dict:
			corr = pearsonr(help_dict[key][0], help_dict[key][1])
			n = key
			help_writer.writerow({'n' : n, 'corr': corr[0], 'p_val' : corr[1]})
	help_file.close()

	with open('../fixtures/all_csv/Comment_history_correlation_Clarity' + switch + '.csv', 'w') as clar_file:
		fieldnames = ['n', 'corr', 'p_val']
		clar_writer = DictWriter(clar_file, fieldnames = fieldnames)
		clar_writer.writeheader()
		for key in clar_dict:
			corr = pearsonr(clar_dict[key][0], clar_dict[key][1])
			n = key
			clar_writer.writerow({'n' : n, 'corr': corr[0], 'p_val' : corr[1]})
	clar_file.close()	

	with open('../fixtures/all_csv/Comment_history_correlation_Easiness' + switch + '.csv', 'w') as ease_file:
		fieldnames = ['n', 'corr', 'p_val']
		ease_writer = DictWriter(ease_file, fieldnames = fieldnames)
		ease_writer.writeheader()
		for key in ease_dict:
			corr = pearsonr(ease_dict[key][0], ease_dict[key][1])
			n = key
			ease_writer.writerow({'n' : n, 'corr': corr[0], 'p_val' : corr[1]})
	ease_file.close()

def get_top_disciplines_division():
	#set_trace()
	top_discs_tuples = get_top_departments(switch = 'D', records = MongoClient()['rmpdb']['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'details': 1, '_id' : 1}))
	csvfile = open('../fixtures/all_csv/Displine_division.csv', 'w')
	fieldnames = ['id', 'city', 'state', 'discipline', 'university', 'gender', 'ovr-quality', 'clarity', 'easiness', 'helpfulness', 'avg-grade-received']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	top_disciplines = list()
	for disc_row in top_discs_tuples:
		top_disciplines.append(disc_row[0].encode('utf-8'))

	
	csvfile.close()

def get_red_blue_states_list():
	"""
	Source: https://en.wikipedia.org/wiki/Red_states_and_blue_states#/media/File:Red_and_Blue_States_Map_(Average_Margins_of_Presidential_Victory).svg
	Returns a list of Republican, Neutral and Democratic states
	"""
	#R, N, D, represent Republican, Neutral and Democratic states
	R = ['UT', 'ID', 'WY', 'NE', 'AK', 'OK', 'KS', 'ND', 'AL', 'TX', 'MS', 'SD', 'SC', 'MT', 'KY', 'IN', 'GA', 'NC', 'TN', 'AZ', 'LA', 'VA']
	N = ['NV', 'WV', 'AR', 'CO', 'FL', 'MO', 'OH']
	D = ['NH', 'IA', 'WI', 'NM', 'PA', 'OR', 'MN', 'MI', 'WA', 'NJ', 'ME', 'DE', 'CA', 'CT', 'IL', 'MD', 'VT', 'HI', 'NY', 'RI', 'MA']
	return (R, N, D)

def get_state_ratings_distribution(profs_cur = None):
	"""
	Get the ratings distribution across Republican, Democratic and Neutral States of US. 
	"""
	set_trace()
	R, N, D = get_red_blue_states_list()

	profs_cur = MongoClient()['rmpdb']['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'ratings' : 1, 'details.state' : 1, 'gender' : 1})
	
	csvfile = open('../fixtures/all_csv/State_division.csv', 'w')
	fieldnames = ['stateAbbr', 'stateColor', 'ovr', 'clarity', 'easiness', 'helpfulness', 'gender']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()

	for prof in profs_cur:
		if prof['details']['state'] in R:
			state_c = 'Republican'
		elif prof['details']['state'] in N:
			state_c = 'Neutral'
		elif prof['details']['state'] in D:
			state_c = 'Democratic'
		else:
			continue
		file_writer.writerow({'stateAbbr' : prof['details']['state'], 
							'stateColor' : state_c, 
							'ovr' : prof['ratings']['overall-quality'],
							'clarity': prof['ratings']['clarity'],
							'easiness': prof['ratings']['easiness'],
							'helpfulness': prof['ratings']['helpfulness'],
							'gender': prof['gender']})

def get_comments_monthly_distribution(comments_cur = None, file_write_switch = True, grades = None):
	"""
	Get the number of reviews as a monthly distribution and store them in a CSV file
	"""
	if comments_cur == None:
		comments_cur = MongoClient()['rmpdb']['comments'].find({'prof_gender' : {'$in' : ['M', 'F']}}, {'prof_gender': 1, 'month' : 1})
		if not grades == None:
			comments_cur = MongoClient()['rmpdb']['comments'].find({'prof_gender' : {'$in' : ['M', 'F']}, 'teacherGrade' : {'$in' : grades}}, {'prof_gender': 1, 'month' : 1})

	male_month_comments_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_month_comments_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	for comment in tqdm(comments_cur):
		if comment['prof_gender'] == 'M':
			male_month_comments_dict[int(comment['month'])] += 1
		else:
			female_month_comments_dict[int(comment['month'])] += 1
	
	if file_write_switch:
		csvfile = open('../fixtures/all_csv/monthly_comments_distribution.csv', 'w')
		fieldnames = ['month', 'num_comments', 'gender']
		file_writer = DictWriter(csvfile, fieldnames = fieldnames)
		file_writer.writeheader()
	
		for month in male_month_comments_dict:
			file_writer.writerow({'month' : month, 'num_comments' : male_month_comments_dict[month], 'gender' : 'M'})
		for month in female_month_comments_dict:
			file_writer.writerow({'month' : month, 'num_comments' : female_month_comments_dict[month], 'gender' : 'F'})

	return (male_month_comments_dict, female_month_comments_dict)

def get_avg_ovr_monthly_distribution(comments_cur = None):
	"""
	Get the clarity, easiness and helpfulness scores distribution by month
	"""
	set_trace()
	if comments_cur == None:
		comments_cur = MongoClient()['rmpdb']['comments'].find({'prof_gender' : {'$in' : ['M', 'F']}}, {'prof_gender': 1, 'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
	
	interest_lookup = {"Meh" : 1, "Low" : 2, "Sorta interested" : 3, "Really into it" : 4, "It's my life" : 5}

	male_monthly_clar_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	female_monthly_clar_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	male_monthly_ease_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	female_monthly_ease_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	male_monthly_help_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	female_monthly_help_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	male_monthly_interest_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	female_monthly_interest_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
	
	for comment in comments_cur:
		month = int(comment['month'])
		if comment['prof_gender'] == 'M':
			male_monthly_clar_dict[month].append(int(comment['rClarity']))
			male_monthly_ease_dict[month].append(int(comment['rEasy']))
			male_monthly_help_dict[month].append(int(comment['rHelpful']))
			if comment['rInterest'].encode('utf-8') in interest_lookup:
				male_monthly_interest_dict[month].append(interest_lookup[comment['rInterest'].encode('utf-8')])
		else:
			female_monthly_clar_dict[month].append(int(comment['rClarity']))
			female_monthly_ease_dict[month].append(int(comment['rEasy']))
			female_monthly_help_dict[month].append(int(comment['rHelpful']))
			if comment['rInterest'].encode('utf-8') in interest_lookup:
				female_monthly_interest_dict[month].append(interest_lookup[comment['rInterest'].encode('utf-8')])

	csvfile = open('../fixtures/all_csv/monthly_average_scores_distribution.csv', 'w')
	fieldnames = ['month', 'avg_clarity', 'avg_easiness', 'avg_helpfulness', 'avg_interest', 'gender']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()

	for (month1, val1), (month2, val2), (month3, val3), (month4, val4), (month5, val5), (month6, val6), (month7, val7), (month8, val8) in zip(male_monthly_clar_dict.items(), male_monthly_ease_dict.items(), male_monthly_help_dict.items(), male_monthly_interest_dict.items(), female_monthly_clar_dict.items(), female_monthly_ease_dict.items(), female_monthly_help_dict.items(), female_monthly_interest_dict.items()):
		
		male_monthly_clar_dict[month1] = sum(val1) / (len(val1) * 1.0)
		male_monthly_ease_dict[month2] = sum(val2) / (len(val2) * 1.0)
		male_monthly_help_dict[month3] = sum(val3) / (len(val3) * 1.0)
		try:
			male_monthly_interest_dict[month4] = sum(val4) / (len(val4) * 1.0)
		except:
			male_monthly_interest_dict[month4] = 0
		
		female_monthly_clar_dict[month5] = sum(val5) / (len(val5) * 1.0)
		female_monthly_ease_dict[month6] = sum(val6) / (len(val6) * 1.0)
		female_monthly_help_dict[month7] = sum(val7) / (len(val7) * 1.0)
		try:
			female_monthly_interest_dict[month8] = sum(val8) / (len(val8) * 1.0)
		except:
			female_monthly_interest_dict[month8] = 0
	
	for month in male_monthly_clar_dict:
		file_writer.writerow({'month' : month, 'avg_clarity' : male_monthly_clar_dict[month], 'avg_easiness' : male_monthly_ease_dict[month], 'avg_helpfulness' : male_monthly_help_dict[month], 'avg_interest' : male_monthly_interest_dict[month], 'gender' : 'M'})
	for month in female_monthly_clar_dict:
		file_writer.writerow({'month' : month, 'avg_clarity' : female_monthly_clar_dict[month], 'avg_easiness' : female_monthly_ease_dict[month], 'avg_helpfulness' : female_monthly_help_dict[month], 'avg_interest' : female_monthly_interest_dict[month], 'gender' : 'F'})

def get_comment_avg_scores_distribution(profs_cur = None, grades = None):
	"""
	"""
	
	conn = MongoClient('mongodb://localhost:27017')
	rmpdb = conn['rmpdb']
	if profs_cur == None:
		profs_cur = rmpdb['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'_id' : 1, 'gender' : 1})

	interest_lookup = {"Meh" : 1, "Low" : 2, "Sorta interested" : 3, "Really into it" : 4, "It's my life" : 5}

	csvfile = open('../fixtures/all_csv/all_comments_month_avg_scores_gender.csv', 'w')
	fieldnames = ['gender', 'month', 'avg_clarity', 'avg_easiness', 'avg_helpfulness', 'avg_interest']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	for prof in tqdm(profs_cur):
		gender = prof['gender']
		if grades == None:
			comments_cur = rmpdb['comments'].find({'prof_id' : str(prof['_id'])}, {'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
		else:
			comments_cur = rmpdb['comments'].find({'prof_id' : str(prof['_id']), 'teacherGrade' : {'$in' : grades}}, {'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
		clar_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		ease_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		help_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		interest_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		for comment in comments_cur:
			month = int(comment['month'])
			if comment['rClarity'] > 0:	
				clar_dict[month].append(comment['rClarity'])
			if comment['rEasy'] > 0:
				ease_dict[month].append(comment['rEasy'])
			if comment['rHelpful'] > 0:
				help_dict[month].append(comment['rHelpful'])
			if comment['rInterest'].encode('utf-8') in interest_lookup:
				interest_dict[month].append(comment['rInterest'])

		for month in clar_dict:
			try:
				clar_dict[month] = sum(clar_dict[month]) / (len(clar_dict[month]) * 1.0)
			except:
				clar_dict[month] = 0.0
			try:
				ease_dict[month] = sum(ease_dict[month]) / (len(ease_dict[month]) * 1.0)
			except:
				ease_dict[month] = 0.0
			try:
				help_dict[month] = sum(help_dict[month]) / (len(help_dict[month]) * 1.0)
			except:
				help_dict[month] = 0.0
			try:
				interest_dict[month] = sum(interest_dict[month]) / (len(interest_dict[month]) * 1.0)
			except:
				interest_dict[month] = 0.0

		for month in clar_dict:
			file_writer.writerow({
				'gender' : gender,
				'month' : month,
				'avg_clarity' : clar_dict[month],
				'avg_easiness' : ease_dict[month],
				'avg_helpfulness' : help_dict[month],
				'avg_interest' : interest_dict[month]
				})



def get_best_worst_ratings_monthly_distribution(profs_cur = None, grades = None):
	"""
	"""
	conn = MongoClient('mongodb://localhost:27017')
	rmpdb = conn['rmpdb']

	male_all_month_comments_dict, female_all_month_comments_dict = get_comments_monthly_distribution(file_write_switch = False, grades = grades)

	all_month_comments_dict = dict()
	for month in male_all_month_comments_dict:
		all_month_comments_dict[month] = male_all_month_comments_dict[month] + female_all_month_comments_dict[month]

	if profs_cur == None:
		profs_cur = rmpdb['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'_id' : 1, 'gender' : 1})
	#
	interest_lookup = {"Meh" : 1, "Low" : 2, "Sorta interested" : 3, "Really into it" : 4, "It's my life" : 5}
	
	male_best_clar_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_best_help_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_best_ease_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_best_interest_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_best_clar_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_best_help_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_best_ease_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_best_interest_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

	male_worst_clar_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_worst_help_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_worst_ease_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	male_worst_interest_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_worst_clar_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_worst_help_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_worst_ease_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
	female_worst_interest_dict = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

	for prof in tqdm(profs_cur):
		try:
			gender = prof['gender']
			if grades == None:
				comments_cur = rmpdb['comments'].find({'prof_id' : str(prof['_id'])}, {'prof_gender' : 1, 'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
				comments_cur_copy = rmpdb['comments'].find({'prof_id' : str(prof['_id'])}, {'prof_gender' : 1, 'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
			else:
				comments_cur = rmpdb['comments'].find({'prof_id' : str(prof['_id']), 'teacherGrade' : {'$in' : grades}}, {'prof_gender' : 1, 'month' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})

			if comments_cur.count() == 0:
				continue

			clar_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
			ease_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
			help_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
			interest_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

			#Store the scores for each comment in scoring lists by month
			for comment in comments_cur:
				month = int(comment['month'])
				clar_dict[month].append(comment['rClarity'])
				ease_dict[month].append(comment['rEasy'])
				help_dict[month].append(comment['rHelpful'])
				if comment['rInterest'].encode('utf-8') in interest_lookup:
					interest_dict[month].append(interest_lookup[comment['rInterest'].encode('utf-8')])
			#Find monthwise average score for each scoring list
			for month in clar_dict:
				try:
					clar_dict[month] = sum(clar_dict[month]) / (len(clar_dict[month]) * 1.0)
				except:
					clar_dict[month] = -1
				try:
					ease_dict[month] = sum(ease_dict[month]) / (len(ease_dict[month]) * 1.0)
				except:
					ease_dict[month] = -1
				try:
					help_dict[month] = sum(help_dict[month]) / (len(help_dict[month]) * 1.0)
				except:
					help_dict[month] = -1
				try:
					interest_dict[month] = sum(interest_dict[month]) / (len(interest_dict[month]) * 1.0)
				except:
					interest_dict[month] = -1
			#Find best performing month for each scoring list
			sorted_clar_dict = sorted(clar_dict.items(), key = itemgetter(1), reverse = True)
			sorted_ease_dict = sorted(ease_dict.items(), key = itemgetter(1), reverse = True)
			sorted_help_dict = sorted(help_dict.items(), key = itemgetter(1), reverse = True)
			sorted_interest_dict = sorted(interest_dict.items(), key = itemgetter(1), reverse = True)

			clar_best_month = sorted_clar_dict[0][0]
			while sorted_clar_dict[-1][1] < 0:
				sorted_clar_dict.pop()
			try:
				clar_worst_month = sorted_clar_dict[-1][0]
			except:
				pass
			
			ease_best_month = sorted_ease_dict[0][0]
			while sorted_ease_dict[-1][1] < 0:
				sorted_ease_dict.pop()
			try:
				ease_worst_month = sorted_ease_dict[-1][0]
			except:
				pass
		
			help_best_month = sorted_help_dict[0][0]
			while sorted_help_dict[-1][1] < 0:
				sorted_help_dict.pop()
			try:
				help_worst_month = sorted_help_dict[-1][0]
			except:
				pass
			
			#Check out interest_best_month heren	
			if sorted_interest_dict[0][1] == -1:
				interest_null_flag = True
				interest_best_month = None
				interest_worst_month = None
			else:	
				interest_null_flag = False
				interest_best_month = sorted_interest_dict[0][0]
				while sorted_interest_dict[-1][1] < 0:
					sorted_interest_dict.pop()
				try:
					interest_worst_month = sorted_interest_dict[-1][0]
				except:
					pass

			if gender == 'M':
				male_best_clar_dict[clar_best_month] += 1
				male_worst_clar_dict[clar_worst_month] += 1
				male_best_ease_dict[ease_best_month] += 1
				male_worst_ease_dict[ease_worst_month] += 1
				male_best_help_dict[help_best_month] += 1
				male_worst_help_dict[help_worst_month] += 1
				if not interest_null_flag:
					male_best_interest_dict[interest_best_month] += 1
					male_worst_interest_dict[interest_worst_month] += 1
			else:
				female_best_clar_dict[clar_best_month] += 1
				female_worst_clar_dict[clar_worst_month] += 1
				female_best_ease_dict[ease_best_month] += 1
				female_worst_ease_dict[ease_worst_month] += 1
				female_best_help_dict[help_best_month] += 1
				female_worst_help_dict[help_worst_month] += 1
				if not interest_null_flag:
					female_best_interest_dict[interest_best_month] += 1
					female_worst_interest_dict[interest_worst_month] += 1

		except:
			print str(prof['_id'])

	set_trace()
	for month in male_best_clar_dict:
		male_best_clar_dict[month] = male_best_clar_dict[month] / (all_month_comments_dict[month] * 1.0) 
		male_worst_clar_dict[month] = male_worst_clar_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_best_ease_dict[month] = male_best_ease_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_worst_ease_dict[month] = male_worst_ease_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_best_help_dict[month] = male_best_help_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_worst_help_dict[month] = male_worst_help_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_best_interest_dict[month] = male_best_interest_dict[month] / (all_month_comments_dict[month] * 1.0)
		male_worst_interest_dict[month] = male_worst_interest_dict[month] / (all_month_comments_dict[month] * 1.0)

		female_best_clar_dict[month] = female_best_clar_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_worst_clar_dict[month] = female_worst_clar_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_best_ease_dict[month] = female_best_ease_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_worst_ease_dict[month] = female_worst_ease_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_best_help_dict[month] = female_best_help_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_worst_help_dict[month] = female_worst_help_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_best_interest_dict[month] = female_best_interest_dict[month] / (all_month_comments_dict[month] * 1.0)
		female_worst_interest_dict[month] = female_worst_interest_dict[month] / (all_month_comments_dict[month] * 1.0)


	#csvfile
	csvfile = open('../fixtures/all_csv/monthwise_best_worst_scores_distribution_MFprofs.csv', 'w')
	fieldnames = ['month', 'gender', 'best_clarity', 'worst_clarity', 'best_easiness', 'worst_easiness', 'best_helpfulness', 'worst_helpfulness', 'best_interest', 'worst_interest']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	
	for month in male_best_clar_dict:
		file_writer.writerow({
			'month'	:month,
			'gender'	:'M',
			'best_clarity': male_best_clar_dict[month],
			'worst_clarity': male_worst_clar_dict[month],
			'best_easiness': male_best_ease_dict[month],
			'worst_easiness': male_worst_ease_dict[month],
			'best_helpfulness': male_best_help_dict[month],
			'worst_helpfulness': male_worst_help_dict[month],
			'best_interest': male_best_interest_dict[month],
			'worst_interest': male_worst_interest_dict[month]})

	for month in female_best_clar_dict:
		file_writer.writerow({
			'month'	:month,
			'gender'	:'F',
			'best_clarity': female_best_clar_dict[month],
			'worst_clarity': female_worst_clar_dict[month],
			'best_easiness': female_best_ease_dict[month],
			'worst_easiness': female_worst_ease_dict[month],
			'best_helpfulness': female_best_help_dict[month],
			'worst_helpfulness': female_worst_help_dict[month],
			'best_interest': female_best_interest_dict[month],
			'worst_interest': female_worst_interest_dict[month]})

def get_dem_repub_word_distribution(profs_cur = None):
	"""
	"""
	set_trace()
	
	from nltk.corpus import stopwords
	cached_stops = stopwords.words('english')

	R, N, D = get_red_blue_states_list()
	if profs_cur == None:
		profs_cur = MongoClient()['rmpdb']['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'all comments.rComments' : 1, 'details.state' : 1, 'gender' : 1})
	R_male = open('Republican_Male_Comments.txt', 'w')
	R_female = open('Republican_Female_Comments.txt', 'w')
	D_male = open('Democrat_Male_Comments.txt', 'w')
	D_female = open('Democrat_Female_Comments.txt', 'w')
	for prof in profs_cur:
		for comment in prof['all comments']:
			text_comment = comment['rComments'].encode('utf-8').lower()
			text_comment = ''.join([l for l in text_comment if l not in ('!', '.', '?', ':', ';', '&', '<', '>', '#', '$', '%', '^', '*', '(', ')', '-', ':', '"', "'", ',', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'quot')])
			text_comment = ' '.join([word for word in text_comment.split() if word not in cached_stops])
			if prof['details']['state'] in R:
				if prof['gender'] == 'M':
					R_male.write(text_comment + '\n')
				else:					
					R_female.write(text_comment + '\n')
			elif prof['details']['state'] in D:
				if prof['gender'] == 'M':
					D_male.write(text_comment + '\n')
				else:
					D_female.write(text_comment + '\n')
			else:
				continue

def normalize_word_count(filename, color):
    from collections import Counter
    from random import shuffle
    word_dict = Counter()
    with open(filename) as in_file:
        # iterate over each line
        for line in in_file:
            # pass each stripped word from the line to the Counter dict
            word_dict.update(x for x in line.split())
    sorted_word_dict = sorted(word_dict.items(), key = itemgetter(1), reverse = True)
    with open(filename + '.csv', 'w') as out_file:
    	count = 0
    	for item in sorted_word_dict:
    		
    		if item[1] <= 1000 or count == 500:
    			break
    		out_file.write(item[0] + ';' + str(item[1] / 1000) + ';' + color + ';' + '0' ';' + 'PT Sans Regular' + ';' + '0' + ';'  + '' +'\n')
    		count += 1
    '''set_trace()
    shuffle(sorted_word_dict)
    with open('mini_' + filename, 'w') as out_file:
    	count = 0
    	for item in sorted_word_dict[:50]:
    		normal = item[1]
    		out_file.write((item[0] + ' ') * normal)'''
    		
def get_top_of_top_20_tags(profs_cur = None):
	"""
	"""
	set_trace()
	if profs_cur == None:
		conn = MongoClient('mongodb://localhost:27017')
		rmpdb = conn['rmpdb']
		profs_cur = rmpdb['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'_id' : 0, 'gender' : 1, 'top 20 tags' : 1})

	m_tags = {}
	f_tags = {}

	for prof in profs_cur:
		tags = prof['top 20 tags']

		if len(tags) == 0:
			continue
		
		if len(tags) > 3:
			top_3_tags = tags[:3]
		else:
			top_3_tags = tags

		if prof['gender'] == 'M':
			for tag in top_3_tags:
				if tag['tag-name'] in m_tags:
					m_tags[tag['tag-name']] += 1
				else:
					m_tags[tag['tag-name']] = 1
		else:
			for tag in top_3_tags:
				if tag['tag-name'] in f_tags:
					f_tags[tag['tag-name']] += 1
				else:
					f_tags[tag['tag-name']] = 1

	csvfile = open('../fixtures/all_csv/male_top_20_tags.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	for tag in m_tags:
		file_writer.writerow({
			'Word' : tag, 
			'Weight' : m_tags[tag], 
			'Color' : '0000ff', 
			'Angle' : 0, 
			'Font' : 'PT Sans Regular', 
			'Repeat?' : 0})
	csvfile.close()

	csvfile = open('../fixtures/all_csv/female_top_20_tags.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	for tag in f_tags:
		file_writer.writerow({
			'Word' : tag, 
			'Weight' : f_tags[tag], 
			'Color' : 'ff0000', 
			'Angle' : 0, 
			'Font' : 'PT Sans Regular', 
			'Repeat?' : 0})
	csvfile.close()

	return(m_tags, f_tags)

def get_tag_distribution(comments_cur = None):
	"""
	"""
	if comments_cur == None:
		conn = MongoClient('mongodb://localhost:27017')
		rmpdb = conn['rmpdb']
		comments_cur = rmpdb['comments'].find({'prof_gender' : {'$in' : ['M', 'F']}}, {'_id' : 0, 'prof_gender' : 1, 'teacherRatingTags' : 1})

	m_tags = dict()
	f_tags = dict()

	for comment in tqdm(comments_cur):
		tags = comment['teacherRatingTags']
		if comment['prof_gender'] == 'M':
			for tag in tags:
				if tag in m_tags:
					m_tags[tag] += 1
				else:
					m_tags[tag] = 1
		else:
			for tag in tags:
				if tag in f_tags:
					f_tags[tag] += 1
				else:
					f_tags[tag] = 1


	csvfile = open('../fixtures/all_csv/male_tags_distribution.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in m_tags:
		file_writer.writerow({
			'Word' : tag, 
			'Weight' : m_tags[tag], 
			'Color' : '0000ff', 
			'Angle' : 0, 
			'Font' : 'PT Sans Regular', 
			'Repeat?' : 0})
	csvfile.close()

	csvfile = open('../fixtures/all_csv/female_tags_distribution.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in f_tags:
		file_writer.writerow({
			'Word' : tag, 
			'Weight' : f_tags[tag], 
			'Color' : 'ff0000', 
			'Angle' : 0, 
			'Font' : 'PT Sans Regular', 
			'Repeat?' : 0})
	csvfile.close()

def get_range(score):
	if score >= 1.0 and score <=1.5:
		r = '1-1.5'
	elif score > 1.5 and score <= 2.0:
		r = '1.5-2'
	elif score > 2.0 and score <= 2.5:
		r = '2-2.5'
	elif score > 2.5 and score <= 3.0:
		r = '2.5-3'
	elif score > 3.0 and score <= 3.5:
		r = '3-3.5'
	elif score > 3.5 and score <= 4.0:
		r = '3.5-4'
	elif score > 4.0 and score <= 4.5:
		r = '4-4.5'
	else:
		if score == 0:
			r = None
		else:
			r = '4.5-5'

	return r

def get_month(month):
	mdict = {	1 : 'jan', 2 : 'feb', 3 : 'mar', 4 : 'apr', 5 : 'may', 6 : 'jun',
				7 : 'jul', 8 : 'aug', 9 : 'sep', 10: 'oct', 11 : 'nov', 12 : 'dec'}

	return mdict[month]

def gen_month_average_rating_heatmap():
	"""
	"""
	from RMP_metadata import interest_lookup
	jan_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	feb_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	mar_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	apr_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	may_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	jun_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	jul_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	aug_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	sep_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	oct_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	nov_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}
	dec_dict = {'1-1.5': 0, '1.5-2': 0, '2-2.5':0, '2.5-3':0, '3-3.5':0, '3.5-4':0, '4-4.5':0, '4.5-5':0}

	data_dict = {'jan':jan_dict, 'feb':feb_dict, 'mar':mar_dict, 'apr':apr_dict, 'may':may_dict, 'jun':jun_dict, 'jul':jul_dict, 'aug':aug_dict, 'sep':sep_dict, 'oct':oct_dict, 'nov':nov_dict, 'dec':dec_dict}
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	profs_cur = rmpdb['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'_id' : 1})
	for prof in tqdm(profs_cur):
		id_string = str(prof['_id'])
		faux_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[]}
		comments_cur = rmpdb['comments'].find({'prof_id' : id_string}, {'_id' : 0, 'rInterest' : 1, 'month' : 1})
		for comment in comments_cur:
			try:
				faux_dict[int(comment['month'])].append(interest_lookup[comment['rInterest']])
			except:
				continue
		for key in faux_dict:
			month_code = get_month(key)
			try:
				range_code = get_range((sum(faux_dict[key]) * 1.0) / len(faux_dict[key]))
				data_dict[month_code][range_code] += 1
			except:
				continue
	csvfile = open('../fixtures/all_csv/interest_heatmap.csv', 'w')
	fieldnames = ['month', '1-1.5', '1.5-2', '2-2.5', '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	for code in data_dict:
		file_writer.writerow({'month' : code,
								'1-1.5' : data_dict[code]['1-1.5'], 
								'1.5-2' : data_dict[code]['1.5-2'], 
								'2-2.5' : data_dict[code]['2-2.5'], 
								'2.5-3' : data_dict[code]['2.5-3'], 
								'3-3.5' : data_dict[code]['3-3.5'], 
								'3.5-4' : data_dict[code]['3.5-4'],
								'4-4.5' : data_dict[code]['4-4.5'], 
								'4.5-5' : data_dict[code]['4.5-5']})

def gen_sentiment_by_comments_data():
	"""
	"""
	from vaderSentiment.vaderSentiment import sentiment
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	profs_cur = rmpdb['profs'].find({'gender' : {'$in' : ['M', 'F']}}, {'gender' : 1, 'ratings.overall-quality' : 1}, no_cursor_timeout = True)
	csvfile = open('../fixtures/all_csv/sentiment_v_overall.csv', 'w')
	fieldnames = ['gender', 'overall', 'positive', 'negative']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames)
	file_writer.writeheader()
	for prof in tqdm(profs_cur):
		id_string = str(prof['_id'])
		overall = prof['ratings']['overall-quality']
		if float(overall) < 1:
			continue
		gender = prof['gender']
		comments_cur = rmpdb['comments'].find({'prof_id' : id_string}, {'_id' : 0, 'rComments' : 1}, no_cursor_timeout = True)
		pos = list()
		neg = list()
		for comment in comments_cur:
			vs = sentiment(comment['rComments'].encode('utf-8'))
			pos.append(vs['pos'])
			neg.append(vs['neg'])
		try:
			pos = (sum(pos) * 1.0) / len(pos)
			neg = (sum(neg) * 1.0) / len(neg)
			file_writer.writerow(	{'gender' : gender,
									'overall' : overall,
									'positive' : pos,
									'negative' : neg})
		except:
			continue

def div_dataset():
	"""
	Divide dataset into professors with more than 10 comments
	"""
	from bson.objectid import ObjectId
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	profs = rmpdb['profs']
	dataset_profs_cur = rmpdb['dataset_profs'].find({}, {'_id' : 0})
	for row in tqdm(dataset_profs_cur):
		prof_id = row['prof_id']
		comments = profs.find_one({'_id' : ObjectId(prof_id)})['all comments']
		if len(comments) < 20:
			rmpdb['dataset_profs_less_twenty'].insert_one(row)
		else:
			rmpdb['dataset_profs_twenty_over'].insert_one(row)








	

def csvcleaner():
	from glob import glob
	import os
	for filename in glob('../fixtures/all_csv/Comment_history*'):
		f_in = open(filename, 'r')
		f_out = open(filename + '.temp', 'w')
		for line in f_in.readlines():
			line_split = line[:-1].split(',')
			if 'nan' in line_split:
				continue
			else:
				f_out.write(line)
		f_in.close()
		f_out.close()
		#os.remove(filename)
		#os.rename(filename + '.temp', filename)
		print 'Rewrote file: ' + filename
