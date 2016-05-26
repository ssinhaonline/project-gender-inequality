from tqdm import tqdm

variable_lookup = [	('1' , 'clarity'),
					('2' , 'easiness'), 
					('3' , 'helpfulness'), 
					('4' , 'interest_level'), 
					('5' , 'overall_quality'),
					('6' , 'state'), 
					('7' , 'discipline'), 
					('8' , 'pos_pos_bigram_count'),
					('9' , 'pos_neu_bigram_count'),
					('10' , 'pos_neg_bigram_count'),
					('11' , 'neu_pos_bigram_count'),
					('12' , 'neu_neu_bigram_count'),
					('13' , 'neu_neg_bigram_count'),
					('14' , 'neg_pos_bigram_count'),
					('15' , 'neg_neu_bigram_count'),
					('16' , 'neg_neg_bigram_count'),
					('17' , 'clar_history_corr'),
					('18' , 'ease_history_corr'),
					('19' , 'help_history_corr'),
					('20' , 'comment_positivity_corr'),
					('21' , 'comment_negativity_corr'),
					('22' , 'interest_history_corr'),
					('23' , 'num_comments'),
					('24' , 'num_commas'),
					('25' , 'num_quotes'),
					('26' , 'num_semicolons'),
					('27' , 'num_colons'),
					('28' , 'num_pauses'),
					('29' , 'num_questions'),
					('30' , 'num_exclamations'),
					('31' , 'ADV'),
					('32' , 'NOUN'),
					('33' , 'ADP'),
					('34' , 'PRT'),
					('35' , 'DET'),
					('36' , 'PRON'),
					('37' , 'VERB'),
					('38' , 'NUM'),
					('39' , 'CONJ'),
					('40' , 'ADJ'),
					('41' , '.'),
					('42' , 'X'),
					('43' , 'num_unq_words'),
					('44' , 'num_positive_words'),
					('45' , 'num_negative_words'),
					('46' , 'num_positive_comments'),
					('47' , 'num_negative_comments'),
					('48' , 'ratio_pos_neg_words'),
					('49' , 'ratio_pos_neg_comments'),
					('50' , 'std_clarity'),
					('51' , 'std_easiness'),
					('52' , 'std_helpfulness'),
					('53' , 'std_interest_level'),
					('class' , 'gender')]


def build_initial_ds():
	"""
	Build basic dataset for variables 1 through 7
	"""
	from pymongo import MongoClient
	#from RMP_gender_stats import get_prof_average_interest
	from RMP_metadata import dept_dict, state_dict, gender_lookup, interest_lookup
	from pdb import set_trace
	from numpy import mean, std

	set_trace()

	conn = MongoClient('mongodb://localhost:27017')
	rmpdb = conn['rmpdb']
	dataset_coll = rmpdb['dataset_profs_ten_over']
	ds_cur = dataset_coll.find({}, {'_id' : 1, 'prof_id' : 1}, no_cursor_timeout = True)
	# profs_cur = rmpdb['profs'].find({'gender' : 	{'$in' : ['M', 'F']}}, 
	# 														{'ratings.clarity' : 1, 
	# 														'ratings.easiness' : 1, 
	# 														'ratings.helpfulness' : 1, 
	# 														'ratings.overall-quality' : 1, 
	# 														'details.state' : 1,
	# 														'details.department' : 1,
	# 														'gender' : 1})

	for prof in tqdm(ds_cur):											# replace with profs_cur

	 	id_string = prof['prof_id']													# str(prof['_id'])										# Comment identifier for quick lookups
	# 	gender = gender_lookup[prof['gender']] 								# Class gender : M/F
	# 	clarity = prof['ratings']['clarity'] 								# Variable clarity : 1
	# 	easiness = prof['ratings']['easiness'] 								# Variable easiness : 2
	# 	helpfulness = prof['ratings']['helpfulness'] 						# Variable helpfulness : 3
	# 	overall_quality = prof['ratings']['overall-quality']				# Variable overall_quality : 5
		# insertion_dict = {'prof_id' : id_string, '1' : clarity, '2' : easiness, '3' : helpfulness, '5' : overall_quality, 'class' : gender}
		insertion_dict = dict()
		# if prof['details']['state'] in state_dict:
		# 	state = state_dict[prof['details']['state']]					# Variable state : 10 (insert only if in US)
		# 	insertion_dict['10'] = state
		# if prof['details']['department'] in dept_dict:
		# 	discipline = dept_dict[prof['details']['department']]			# Variable discipline : 11 (insert only if in top 71 disciplines)
		# 	insertion_dict['11'] = discipline

		comments_cur = rmpdb['comments'].find({'prof_id' : id_string}, {'_id' : 0, 'rInterest' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1})
			
	
		interest_list = list()
		clar_list = list()
		ease_list = list()
		help_list = list()
		for comment in comments_cur:
			if comment['rInterest'] in interest_lookup:
				interest_list.append(interest_lookup[comment['rInterest']])
			clar_list.append(comment['rClarity'])
			ease_list.append(comment['rEasy'])
			help_list.append(comment['rHelpful'])

		try:
			std_clarity = round(float(std(clar_list)), 2)
			insertion_dict['50'] = std_clarity
		except:
			pass

		try:
			std_easiness = round(float(std(ease_list)), 2)
			insertion_dict['51'] = std_easiness
		except:
			pass

		try:
			std_helpfulness = round(float(std(help_list)), 2)
			insertion_dict['52'] = std_helpfulness
		except:
			pass

		try:
			avg_interest = round(float(mean(interest_list)), 2)
			std_interest = round(float(std(interest_list)), 2)
		except:
			avg_interest = None
			std_interest = None

		interest_level = avg_interest
		#interest_level = get_prof_average_interest(comments_cur) 				# Variable interest_level : 4 (insert only if not None)
		if not interest_level == None:
			insertion_dict['4'] = interest_level
			insertion_dict['53'] = std_interest
		
		dataset_coll.update_one({'_id' : prof['_id']}, {'$set' : insertion_dict})		

def add_bigram_sentiment_features():
	"""
	Add features to dataset which involve sentiment from comments
	"""
	from pymongo import MongoClient
	#import RMP_words_funk
	from RMP_words_funk import get_bigrams, get_bigram_sentiment_distribution
	from tqdm import tqdm
	from pdb import set_trace


	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_cur = rmpdb['dataset_profs'].find({}, {'prof_id' : 1}, no_cursor_timeout = True)
	count = 0
	for row in tqdm(ds_cur):
		try:
			prof_id = row['prof_id']
			comments_cur = rmpdb['comments'].find({'prof_id' : prof_id}, {'_id' : 0, 'rComments' : 1})
			all_comments = list()
			
			for comment in comments_cur:
				all_comments.append(comment['rComments'])
			if not len(all_comments) == 0:
				bigrams = get_bigrams(all_comments)
				bigram_sentiment_distr = get_bigram_sentiment_distribution(bigrams)
				rmpdb['dataset_profs'].update_one({'_id' : row['_id']}, {'$set' :
					{
					'8' : bigram_sentiment_distr[0],
					'9' : bigram_sentiment_distr[1],
					'10' : bigram_sentiment_distr[2],
					'11' : bigram_sentiment_distr[3],
					'12' : bigram_sentiment_distr[4],
					'13' : bigram_sentiment_distr[5],
					'14' : bigram_sentiment_distr[6],
					'15' : bigram_sentiment_distr[7],
					'16' : bigram_sentiment_distr[8]
					}})
		except:
			print row['_id']


def add_comments_history_correlation_features():
	"""
	"""
	from pymongo import MongoClient
	from tqdm import tqdm
	from datetime import datetime
	from RMP_metadata import interest_lookup
	from vaderSentiment.vaderSentiment import sentiment
	from scipy.stats import pearsonr
	from pdb import set_trace

	set_trace()

	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_cur = rmpdb['dataset_profs'].find({}, {'prof_id' : 1}, no_cursor_timeout = True)

	for row in tqdm(ds_cur):
		prof_id = row['prof_id']
		comments_cur = rmpdb['comments'].find({'prof_id' : prof_id}, {'_id' : 0, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1, 'rComments' : 1, 'rDate' : 1})
		comments = list()
		if comments_cur.count() > 2:
			for comment in comments_cur:
				comments.append(comment)

			comments_by_date = sorted(comments, key = lambda x: datetime.strptime(x['rDate'], '%m/%d/%Y'))

			help_list = list()
			clar_list = list()
			ease_list = list()
			interest_list = list()
			comment_positivity_list = list()
			comment_negativity_list = list()
			for comment in comments_by_date:
				help_list.append(float(comment['rHelpful']))
				clar_list.append(float(comment['rClarity']))
				ease_list.append(float(comment['rEasy']))
				if comment['rInterest'] in interest_lookup:
					interest_list.append(interest_lookup[comment['rInterest']])
				sentiments = sentiment(comment['rComments'].encode('utf-8'))
				comment_positivity_list.append(sentiments['pos'])
				comment_negativity_list.append(sentiments['neg'])

			pparam1 = list()
			pparam2 = list()

			for i in range(1, len(help_list)):
				pparam1.append(float(sum(help_list[:i])) / len(help_list[:i]))
				pparam2.append(help_list[i])
			help_history_corr, help_p_val = pearsonr(pparam1, pparam2)

			
			pparam1 = list()
			pparam2 = list()

			for i in range(1, len(ease_list)):
				pparam1.append(float(sum(ease_list[:i])) / len(ease_list[:i]))
				pparam2.append(ease_list[i])
			ease_history_corr, ease_p_val = pearsonr(pparam1, pparam2)

			pparam1 = list()
			pparam2 = list()

			for i in range(1, len(clar_list)):
				pparam1.append(float(sum(clar_list[:i])) / len(clar_list[:i]))
				pparam2.append(clar_list[i])			
			clar_history_corr, clar_p_val = pearsonr(pparam1, pparam2)

			pparam1 = list()
			pparam2 = list()

			for i in range(1, len(comment_positivity_list)):
				pparam1.append(float(sum(comment_positivity_list[:i])) / len(comment_positivity_list[:i]))
				pparam2.append(comment_positivity_list[i])			
			comment_positivity_corr, comment_positivity_p_val = pearsonr(pparam1, pparam2)

			pparam1 = list()
			pparam2 = list()

			for i in range(1, len(comment_negativity_list)):
				pparam1.append(float(sum(comment_negativity_list[:i])) / len(comment_negativity_list[:i]))
				pparam2.append(comment_negativity_list[i])			
			comment_negativity_corr, comment_negativity_p_val = pearsonr(pparam1, pparam2)

			insertion_dict = {	'17' : clar_history_corr,
								'18' : ease_history_corr,
								'19' : help_history_corr,
								'20' : comment_positivity_corr,
								'21' : comment_negativity_corr}

			if len(interest_list) > 2:

				pparam1 = list()
				pparam2 = list()

				for i in range(1, len(interest_list)):
					pparam1.append(float(sum(interest_list[:i])) / len(interest_list[:i]))
					pparam2.append(interest_list[i])			
				interest_history_corr, interest_p_val = pearsonr(pparam1, pparam2)
				insertion_dict['22'] = interest_history_corr

			rmpdb['dataset_profs'].update_one({'_id' : row['_id']}, {'$set' :insertion_dict})	

def update_history_fields():
	from pymongo import MongoClient
	dataset = MongoClient('mongodb://localhost:27017')['rmpdb']['dataset_profs_ten_over']
	cur = dataset.find({},{'17':1,'18':1,'19':1,'20':1,'21':1,'22':1,'48':1,'49':1})
	for row in tqdm(cur):
		_id = row['_id']
		set_dict = dict()
		try:
			f17 = row['17']
			set_dict['17'] = round(f17, 2) / 100
		except:
			pass
		try:
			f18 = row['18']
			set_dict['18'] = round(f18, 2) / 100
		except:
			pass
		try:
			f17 = row['19']
			set_dict['19'] = round(f19, 2) / 100
		except:
			pass
		try:
			f20 = row['20']
			set_dict['20'] = round(f20, 2) / 100
		except:
			pass
		try:
			f17 = row['21']
			set_dict['21'] = round(f21, 2) / 100
		except:
			pass
		try:
			f17 = row['22']
			set_dict['22'] = round(f22, 2) / 100
		except:
			pass
		try:
			f48 = row['48']
			set_dict['48'] = round(f48, 2) / 100
		except:
			pass
		try:
			f49 = row['49']
			set_dict['49'] = round(f49, 2) / 100
		except:
			pass

		dataset.update_one({'_id':row['_id']},{'$set':set_dict})

		



def add_text_features():
	from pymongo import MongoClient
	from bson.objectid import ObjectId
	from RMP_words_funk import get_punctuation_features, get_pos_features, get_general_text_features
	from RMP_metadata import text_features_map
	from tqdm import tqdm
	from pdb import set_trace

	set_trace()
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_profs_ten_over_cur = rmpdb['dataset_profs_five_over_less_ten'].find({},{'prof_id' : 1}, no_cursor_timeout = True)
	fail_counter = 0
	for row in tqdm(ds_profs_ten_over_cur):
		id_string = row['prof_id']
		prof_comments = rmpdb['profs'].find_one({'_id' : ObjectId(id_string)}, {'_id' : 0, 'all comments.rComments' : 1})
		full_text = ''
		for comment in prof_comments['all comments']:
			full_text = full_text + comment['rComments'].encode('utf-8') + ' '

		try:
			num_comments = len(prof_comments['all comments'])
			punctuation_features = get_punctuation_features(full_text)
			pos_features = get_pos_features(full_text)
			general_text_features = get_general_text_features(full_text)

			insertion_dict = dict()
			insertion_dict[str(text_features_map['num_comments'])] = num_comments
			for feature in punctuation_features:
				insertion_dict[str(text_features_map[feature])] = punctuation_features[feature]
			for feature in pos_features:
				insertion_dict[str(text_features_map[feature])] = pos_features[feature]
			for feature in general_text_features:
				insertion_dict[str(text_features_map[feature])] = general_text_features[feature]

			result = rmpdb['dataset_profs_five_over_less_ten'].update_one({'_id' : row['_id']}, {'$set' :insertion_dict})
		except:
			fail_counter += 1
			continue
	print fail_counter

def add_sentiment_comment_features():
	"""
	"""
	from pymongo import MongoClient
	from bson.objectid import ObjectId
	from tqdm import tqdm
	from vaderSentiment.vaderSentiment import sentiment
	from RMP_words_funk import strip_punctuation
	from pdb import set_trace

	set_trace()

	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_profs_ten_over_cur = rmpdb['dataset_profs_five_over_less_ten'].find({},{'prof_id' : 1}, no_cursor_timeout = True)

	for row in tqdm(ds_profs_ten_over_cur):
		id_string = row['prof_id']
		prof_comments = rmpdb['profs'].find_one({'_id' : ObjectId(id_string)}, {'_id' : 0, 'all comments.rComments' : 1})
		tokens = list()
		for comment in prof_comments['all comments']:
			tokens.extend(strip_punctuation(comment['rComments']).split())

		insertion_dict = {	'44' : 0,
							'45' : 0,
							'46' : 0,
							'47' : 0}

		for tok in tokens:
			vs = sentiment(tok.encode('utf-8'))
			if vs['pos'] > vs['neg']:
				insertion_dict['44'] += 1
			elif vs['neg'] > vs['pos']:
				insertion_dict['45'] += 1
			else:
				continue

		for comment in prof_comments['all comments']:
			vs = sentiment(comment['rComments'].encode('utf-8'))
			if vs['pos'] > vs['neg']:
				insertion_dict['46'] += 1
			elif vs['neg'] > vs['pos']:
				insertion_dict['47'] += 1
			else:
				continue
		
		result = rmpdb['dataset_profs_five_over_less_ten'].update_one({'_id' : row['_id']}, {'$set' :insertion_dict})

def add_sentiment_ratio_features():
	from pymongo import MongoClient
	from pdb import set_trace

	set_trace()
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_profs_ten_over_cur = rmpdb['dataset_profs_five_over_less_ten'].find({},{'prof_id' : 1, '44' : 1, '45' : 1, '46' : 1, '47' : 1}, no_cursor_timeout = True)

	for row in tqdm(ds_profs_ten_over_cur):
		row_id = row['_id']
		insertion_dict = dict()

		try:
			pos_neg_words = row['44'] * 1.0 / row['45']
			if pos_neg_words > 0:
				insertion_dict['48'] = pos_neg_words
		except:
			pass
		try:
			pos_neg_comments = row['46'] * 1.0 / row['47']
			if pos_neg_comments > 0:
				insertion_dict['49'] = pos_neg_comments
		except:
			pass
		if not len(insertion_dict) == 0:
			rmpdb['dataset_profs_five_over_less_ten'].update_one({'_id' : row_id},{'$set' : insertion_dict})
		
def get_other_features():
	"""
	Get features 44, 50 - 53
	"""
	from pymongo import MongoClient
	from operator import itemgetter
	from string import punctuation
	from RMP_metadata import interest_lookup
	from pdb import set_trace

	exclude = set(punctuation)
	set_trace()
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	ds_profs_ten_over_cur = rmpdb['dataset_profs_five_over_less_ten'].find({},{'prof_id' : 1}, no_cursor_timeout = True)

	for prof in tqdm(ds_profs_ten_over_cur):
		prof_id = prof['prof_id']
		insertion_dict = dict()

		all_words_list = list()
		clar_list = list()
		ease_list = list()
		help_list = list()
		interest_list = list()

		prof_revs = rmpdb['comments'].find({'prof_id' : prof_id}, {'_id' : 0, 'rComments' : 1, 'rClarity' : 1, 'rEasy' : 1, 'rHelpful' : 1, 'rInterest' : 1})
		for rev in prof_revs:
			no_punc_text = ''.join(ch for ch in rev['rComments'] if ch not in exclude)
			no_punc_text = no_punc_text.lower()
			text_tokens = no_punc_text.split()
			all_words_list.extend(text_tokens)

			try:
				clar_list.append(float(rev['rClarity']))
			except:
				pass
			try:
				ease_list.append(float(rev['rEasy']))
			except:
				pass
			try:
				help_list.append(float(rev['rHelpful']))
			except:
				pass
			try:
				interest_list.append(float(interest_lookup[rev['rInterest']]))
			except:
				pass

		num_unq_words = len(list(set(all_words_list)))
		try:
			clar_std = calebs_std_dev(clar_list)
		except:
			pass
		try:
			ease_std = calebs_std_dev(ease_list)
		except:
			pass
		try:
			help_std = calebs_std_dev(help_list)
		except:
			pass
		try:
			interest_std = calebs_std_dev(interest_list)
		except:
			pass
		
		if num_unq_words == 0:
			pass
		else:
			insertion_dict['44'] = num_unq_words
		if  clar_std == 0.0:
			pass
		else:
			insertion_dict['50'] = clar_std
		if ease_std == 0.0:
			pass
		else:
			insertion_dict['51'] = ease_std
		if help_std == 0.0:
			pass
		else:
			insertion_dict['52'] = help_std
		if  interest_std == 0.0:
			pass
		else:
			insertion_dict['53'] = interest_std
		rmpdb['dataset_profs_five_over_less_ten'].update_one({'_id' : prof['_id']},{'$set' : insertion_dict})

def calebs_average(s): 
	"""
	Credits Caleb Madrigal
	"""
	return sum(s) * 1.0 / len(s)

def calebs_std_dev(s):
	"""
	Credits Caleb Madrigal
	"""
	import math
	avg = calebs_average(s)
	variance = map(lambda x: (x - avg)**2, s)
	standard_deviation = math.sqrt(calebs_average(variance))
	return standard_deviation

def get_word_vector_features(dataset_cur = None):
	"""
	"""
	from pymongo import MongoClient
	from bson.objectid import ObjectId
	from RMP_words_funk import get_word_vector
	from json import dumps
	from os import remove
	from pdb import set_trace

	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	if dataset_cur ==  None:
		dataset_cur = rmpdb['dataset_profs_less_five'].find({}, {'_id' : 0, 'prof_id' : 1, 'class' : 1}, no_cursor_timeout = True)

	all_male_comments = open('../fixtures/tmp/male_comments.tmp', 'w')
	all_female_comments = open('../fixtures/tmp/female_comments.tmp', 'w')

	for row in tqdm(dataset_cur):
		prof_comments = rmpdb['profs'].find_one({'_id' : ObjectId(row['prof_id'])}, {'_id' : 0, 'all comments.rComments' : 1})
		if row['class'] == 0:
			for comment in prof_comments['all comments']:
				try:
					all_male_comments.write(comment['rComments'])
				except:
					pass
		else:
			for comment in prof_comments['all comments']:
				try:
					all_female_comments.write(comment['rComments'])
				except:
					pass

	
	all_male_comments.close()
	all_female_comments.close()

	all_male_comments = open('../fixtures/tmp/male_comments.tmp', 'r')
	all_female_comments = open('../fixtures/tmp/female_comments.tmp', 'r')

	male_string = all_male_comments.read()
	female_string = all_female_comments.read()

	all_male_comments.close()
	all_female_comments.close()
	remove('../fixtures/tmp/male_comments.tmp')
	remove('../fixtures/tmp/female_comments.tmp')

	male_vector = get_word_vector(male_string)
	female_vector = get_word_vector(female_string)

	fname = raw_input('Vectors generated. Save into: ../logs/')
	f = open('../logs/' + fname + '.vec', 'w')
	f.write(dumps((male_vector, female_vector)))
	f.close()
	return (male_vector, female_vector)

def build_vector():
	"""
	"""
	from pymongo import MongoClient

	ch = raw_input('Select comment cut off for word vectorization (5/10/20) [5]: ')
	if ch == '10':
		ds = 'dataset_profs_less_ten'
	elif ch == '20':
		ds = 'dataset_profs_less_twenty'
	else:
		ds = 'dataset_profs_less_five'
	
	rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
	dataset_cur = rmpdb[ds].find({}, {'_id' : 0, 'prof_id' : 1, 'class' : 1})
	return get_word_vector_features(dataset_cur)


def isNan(x):
	return x != x

def build_svm_file(X, Y):
	"""
	Build an SVM compatible dataset file at liblinear-2.1/ as per the X and Y received
	"""
	f = open('./liblinear-2.1/temp_ds', 'w')
	for x, y in tqdm(zip(X, Y)):
		rowstr = ''

		for key in sorted(x):
			rowstr += str(key) + ':' + str(x[key]) + ' '
		rowstr2 = rowstr[:-1] + '\n'
		if y == 1:
			rowstr2 = '+1 ' + rowstr2
		else:
			rowstr2 = '-1 ' + rowstr2
		f.write(rowstr2)
	f.close()



def classify(ds_cur = None):
	from os import chdir, system
	chdir('./liblinear-2.1/python/')
	from liblinearutil import problem, parameter, train, predict
	chdir('../../')
	from pdb import set_trace
	from tqdm import tqdm
	from pymongo import MongoClient
	from json import dumps
	from bson.objectid import ObjectId

	set_trace()

	dont_include = {'_id' : 0}
	print 'List of variables:\n'
	for key in variable_lookup:
		print key[1]
	ch1 = raw_input('Input "s" to select custom fields (default selection - all fields):')
	if ch1 == 's':
		print 'Please input 0 for fields you would like to exclude, any other input would include it.'
		for key in variable_lookup:
			if key[0] == 'class':
				continue
			ch2 = raw_input(key[1] + ':')
			if ch2 == '0':
				dont_include[key[0]] = 0

	if ds_cur == None:
		conn = MongoClient('mongodb://localhost:27017')
		dataset = conn['rmpdb']['dataset_profs_ten_over']
		ds_cur = dataset.find(filter = {}, projection = dont_include)
		dataset2 = conn['rmpdb']['dataset_profs_five_over_less_ten']
		ds_cur2 = dataset2.find(filter = {}, projection = dont_include)

	X = [] # Variables
	Y = [] # Classes
	ids = [] # Keep track of professor IDs
	X2 = [] # Variables
	Y2 = [] # Classes
	ids2 = [] # Keep track of professor IDs
	

	print 'Building training set according to selection..'
	for row in tqdm(ds_cur):
		x_dict = dict()
		for key in row:
			if key == 'class':
				Y.append(int(row[key]))
			elif key == 'prof_id':
				ids.append(row[key])
			elif isNan(row[key]):
				continue
			else:
				x_dict[int(key)] = float(row[key])
		X.append(x_dict)

	for row in tqdm(ds_cur2):
		x_dict2 = dict()
		for key in row:
			if key == 'class':
				Y2.append(int(row[key]))
			elif key == 'prof_id':
				ids2.append(row[key])
			elif isNan(row[key]):
				continue
			else:
				x_dict2[int(key)] = float(row[key])
		X2.append(x_dict2)

	ch = raw_input('Include top words for males and females as features? (y/n) [n]: ')
	if ch == 'y':
		from glob import glob
		from json import loads

		vec_files = glob('../logs/*.vec')
		if not len(vec_files) == 0:
			print 'Word vector files found in ../logs: \n'
			print vec_files
			fch = raw_input('Enter name of file without extension. [../logs/trial0.vec] Enter 0 to skip. ../logs/')
			if fch == '0':
				male_vector, female_vector = build_vector()
			else:
				try:
					f = open('../logs/' + fch + '.vec', 'r')
					male_vector, female_vector = loads(f.read())
				except:
					f = open('../logs/trial0.vec', 'r')
					male_vector, female_vector = loads(f.read())
		else:
			male_vector, female_vector = build_vector()
		
		print 'Male vectors as (word, count)'
		print male_vector
		print "============================================="
		print 'Female vectors as (word, count)'
		print female_vector
		print "============================================="
		print 'Calculating word features for all professors in dataset. This shall take some time.'
		print 'Depending on your cutoff, this can take from 4 - 6 hours. Probably a good idea to get some other stuff done..'

		male_words = [tup[0] for tup in male_vector]
		female_words = [tup[0] for tup in female_vector]

		union_words = list(set(male_words).union(set(female_words)))
		final_words = list()
		print 'Select words you want to remove by entering "x".'
		for word in union_words:
			wch = raw_input(word + ':')
			if wch == 'x':
				continue
			else:
				final_words.append(word)



		from string import punctuation

		exclude = set(punctuation)
		rmpdb = MongoClient('mongodb://localhost:27017')['rmpdb']
		for i in tqdm(range(len(ids))):
			prof_id = ids[i]

			# male_dict = dict()
			# female_dict = dict()

			# for tup in male_vector:
			# 	male_dict[tup[0]] = 0
			# for tup in female_vector:
			# 	female_dict[tup[0]] = 0

			vec_dict = dict()
			for word in final_words:
				vec_dict[word] = 0

			prof_comments = rmpdb['profs'].find_one({'_id' : ObjectId(prof_id)}, {'_id' : 0, 'all comments.rComments' : 1})
			for comment in prof_comments['all comments']:
				text = comment['rComments']
				no_punc_text = ''.join(ch for ch in text if ch not in exclude)
				toks = no_punc_text.split()

				for tok in toks:
					# if tok.lower() in male_dict:
					# 	male_dict[tok.lower()] += 1
					# if tok.lower() in female_dict:
					# 	female_dict[tok.lower()] += 1
					if tok.lower() in vec_dict:
						vec_dict[tok.lower()] += 1

			feature_counter = 53 #starts right after variable_lookup['53']
			# for j in range(len(male_vector)):
			# 	feature_counter += 1
			# 	tup = male_vector[j]
			# 	if not male_dict[tup[0]] == 0:
			# 		X[i][feature_counter] = male_dict[tup[0]]
			# for j in range(len(female_vector)):
			# 	feature_counter += 1
			# 	tup = female_vector[j]
			# 	if not female_dict[tup[0]] == 0:
			# 		X[i][feature_counter] = female_dict[tup[0]]		
			for j in range(len(final_words)):
				feature_counter += 1
				word = final_words[j]
				if not vec_dict[word] == 0:
					X[i][feature_counter] = vec_dict[word]
				# if feature_counter == 97:
				# 	break

		print "Building test set.."
		for i in tqdm(range(len(ids2))):
			prof_id = ids2[i]

			# male_dict = dict()
			# female_dict = dict()

			# for tup in male_vector:
			# 	male_dict[tup[0]] = 0
			# for tup in female_vector:
			# 	female_dict[tup[0]] = 0

			vec_dict = dict()
			for word in final_words:
				vec_dict[word] = 0

			prof_comments = rmpdb['profs'].find_one({'_id' : ObjectId(prof_id)}, {'_id' : 0, 'all comments.rComments' : 1})
			for comment in prof_comments['all comments']:
				text = comment['rComments']
				no_punc_text = ''.join(ch for ch in text if ch not in exclude)
				toks = no_punc_text.split()

				for tok in toks:
					# if tok.lower() in male_dict:
					# 	male_dict[tok.lower()] += 1
					# if tok.lower() in female_dict:
					# 	female_dict[tok.lower()] += 1
					if tok.lower() in vec_dict:
						vec_dict[tok.lower()] += 1

			feature_counter = 53 #starts right after variable_lookup['53']
			# for j in range(len(male_vector)):
			# 	feature_counter += 1
			# 	tup = male_vector[j]
			# 	if not male_dict[tup[0]] == 0:
			# 		X[i][feature_counter] = male_dict[tup[0]]
			# for j in range(len(female_vector)):
			# 	feature_counter += 1
			# 	tup = female_vector[j]
			# 	if not female_dict[tup[0]] == 0:
			# 		X[i][feature_counter] = female_dict[tup[0]]		
			for j in range(len(final_words)):
				feature_counter += 1
				word = final_words[j]
				if not vec_dict[word] == 0:
					X2[i][feature_counter] = vec_dict[word]

		print 'Words used:'
		print final_words

	else:
		pass

	print 'Writing temp files for AUC calculation..'
	build_svm_file(X, Y)
	print 'Temp file written..'
	print 'Features used:'
	fstr = list()
	for key in variable_lookup:
		if key[0] in dont_include or key[0] == 'class':
			continue
		else:
			fstr.append(key[1])
	print dumps(fstr)
	print '======================================\n'
	prob = problem(Y, X)
	param = parameter('-s 6 -v 10')
	m = train(prob, param)
	print 'Evaluating..\n'
	system('liblinear-2.1/train -s 6 -v 10 liblinear-2.1/temp_ds')
	model = train(prob, parameter('-s 6 -q'))
	#system('rm liblinear-2.1/temp_ds')

	print 'Testing model on test set..'
	p_Y2, p_acc, p_vals = predict(Y2, X2, model)

	contingency_mat = [[0, 0], [0, 0]]
	for i in range(len(Y2)):
		if (Y2[i] == 0) and (p_Y2[i] == 0):
			contingency_mat[0][0] += 1
		elif (Y2[i] == 0) and (p_Y2[i] == 1):
			contingency_mat[0][1] += 1
		elif (Y2[i] == 1) and (p_Y2[i] == 0):
			contingency_mat[1][0] += 1
		else:
			contingency_mat[1][1] += 1


	return (model, p_acc, contingency_mat)
	# return (model, X2, Y2)
	# return m
	# print 'Enter your test row, press enter to skip field:\n'
	# test_row = dict()
	# for key in variable_lookup:
	# 	if key in dont_include or key == 'class':
	# 		continue
	# 	else:
	# 		user_input = raw_input(variable_lookup[key] + ':')
	# 		if user_input == '':
	# 			continue
	# 		else:
	# 			test_row[int(key)] = float(user_input)
	#x0, max_idx = gen_feature_nodearray(test_row)
	#label = liblinear.predict(m, x0)
	#p_label, p_acc, p_val = predict(Y, X, m, '-b 1')
	#ACC, MSE, SCC = evaluations(Y, p_label)
	#return (ACC, MSE, SCC)

def get_important_features(model, top = 25, words = None):
	'''
	'''
	coefs, b = model.get_decfun(label_idx = 0)
	coef_gender_pairs = list()
	for i in range(len(coefs)):
		coef = coefs[i]
		if coef >= 0:
			coef_gender_pairs.append((coef, i, 'M'))
		else:
			coef_gender_pairs.append((-1.0 * coef, i, 'F'))

	coef_gender_pairs = sorted(coef_gender_pairs, key = lambda x : x[0], reverse = True)

	coef_feature_gender_triads = list()
	
	new_var_lookup = dict()
	for t in variable_lookup:
		new_var_lookup[t[0]] = t[1]

	for pair in coef_gender_pairs:
		feature_num = pair[1]
		if feature_num < 53:
			feature = new_var_lookup[str(feature_num + 1)]
		else:
			feature_num = feature_num - 53
			feature = words[feature_num]

		coef_feature_gender_triads.append((pair[0], feature, pair[2]))
	
	return coef_feature_gender_triads[:top]

def get_imp(coefs, top = 25, words = [u'show', u'go', u'enjoyed', u'feedback', u'explain', u'going', u'pretty', u'teaching', u'interested', u'get', u'quizzes', u'overall', u'every', u'lecture', u'dr', u'cool', u'school', u'ever', u'notes', u'isnt', u'assignments', u'bad', u'stuff', u'fair', u'pass', u'best', u'subject', u'even', u'lots', u'goes', u'learned', u'reading', u'youll', u'attention', u'exam', u'got', u'never', u'points', u'however', u'understanding', u'hours', u'teaches', u'teacher', u'great', u'many', u'study', u'experience', u'credit', u'exams', u'makes', u'tough', u'extra', u'sweet', u'highly', u'put', u'semester', u'learning', u'writing', u'use', u'attendance', u'takes', u'would', u'cares', u'come', u'two', u'much', u'recommend', u'taken', u'wants', u'life', u'knows', u'readings', u'understand', u'instructor', u'midterm', u'work', u'teachers', u'learn', u'fun', u'didnt', u'taking', u'ive', u'give', u'awesome', u'cant', u'something', u'want', u'sense', u'wonderful', u'funny', u'end', u'things', u'make', u'write', u'far', u'amazing', u'answer', u'difficult', u'week', u'lab', u'student', u'youre', u'well', u'person', u'pay', u'worst', u'talk', u'help', u'office', u'knowledgeable', u'expects', u'professors', u'course', u'grades', u'grader', u'questions', u'love', u'still', u'group', u'interesting', u'seems', u'actually', u'better', u'feel', u'willing', u'easy', u'homework', u'gave', u'real', u'tests', u'good', u'read', u'material', u'know', u'bit', u'day', u'like', u'wont', u'helpful', u'always', u'passionate', u'everyone', u'people', u'hard', u'back', u'taught', u'really', u'grading', u'everything', u'papers', u'prof', u'math', u'paper', u'ask', u'teach', u'super', u'anything', u'could', u'times', u'due', u'think', u'first', u'dont', u'grade', u'one', u'doesnt', u'another', u'open', u'little', u'long', u'way', u'final', u'gives', u'lot', u'took', u'loved', u'kind', u'made', u'boring', u'us', u'classes', u'loves', u'clear', u'textbook', u'talking', u'say', u'need', u'also', u'book', u'take', u'online', u'test', u'nice', u'lectures', u'sure', u'though', u'students', u'english', u'problems', u'extremely', u'class', u'professor', u'sometimes', u'definitely', u'time']):
	coef_gender_pairs = list()
	for i in range(len(coefs)):
		coef = coefs[i]
		if coef >= 0:
			coef_gender_pairs.append((coef, i, 'M'))
		else:
			coef_gender_pairs.append((-1.0 * coef, i, 'F'))

	coef_gender_pairs = sorted(coef_gender_pairs, key = lambda x : x[0], reverse = True)

	coef_feature_gender_triads = list()
	
	new_var_lookup = dict()
	for t in variable_lookup:
		new_var_lookup[t[0]] = t[1]

	for pair in coef_gender_pairs:
		feature_num = pair[1]
		if feature_num < 53:
			feature = new_var_lookup[str(feature_num + 1)]
		else:
			feature_num = feature_num - 53
			feature = words[feature_num]

		coef_feature_gender_triads.append((pair[0], feature, pair[2]))
	
	return coef_feature_gender_triads[:top]


if __name__ == '__main__':
	classify()
