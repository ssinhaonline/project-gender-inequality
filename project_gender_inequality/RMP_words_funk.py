#!/usr/bin/env python

# Adopted from http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
def get_tokens(text):
	"""
	Tokenize all words in the input file and return word tokens
	"""
	from nltk import word_tokenize
	from string import punctuation
	
	lowers = text.lower()
	no_punc = lowers.translate(None, punctuation)
	tokens = word_tokenize(no_punc)
	return tokens

def remove_stopwords(tokens):
	"""
	Remove stopwords in input tokens and return the filtered tokens
	"""
	from nltk.corpus import stopwords
	cached_stops = stopwords.words('english')

	filtered_tokens = [word for word in tokens if not word in cached_stops]
	return filtered_tokens

def get_word_count(tokens):
	"""
	Return a dictionary containing the word counts in input tokens
	"""
	from collections import Counter

	count = Counter(tokens)
	return count

def stem_tokens(tokens):
	"""
	Return stemmed input tokens using Porter Stemmer
	"""
	from nltk.stem.porter import PorterStemmer
	
	stemmer = PorterStemmer()
	stemmed = []
	
	for word in tokens:
		stemmed.append(stemmer.stem(word))

	return stemmed

def divide_comments_by_gender():
	from pymongo import MongoClient

	conn = MongoClient('mongodb://localhost:27017')
	rmpdb = conn['rmpdb']
	mfile = open('../fixtures/all_txt/comments_male.txt', 'w')
	ffile = open('../fixtures/all_txt/comments_female.txt', 'w')
	comments_cur = rmpdb['comments'].find({'prof_gender' : {'$in' : ['M', 'F']}}, {'prof_gender' : 1, 'rComments' : 1, '_id' : 0})
	for comment in comments_cur:
		if comment['prof_gender'] == 'M':
			mfile.write(comment['rComments'].encode('utf-8') + '\n')
		else:
			ffile.write(comment['rComments'].encode('utf-8') + '\n')

	mfile.close()
	ffile.close()

def clean_stem_file(dirpath, filename):
	
	from tqdm import tqdm
	infile = open(dirpath + filename, 'r')
	outfile = open(dirpath + 'cleaned_stemmed_' + filename, 'w')

	for line in tqdm(infile.readlines()):
		try:
			stem_clean_toks = stem_tokens(remove_stopwords(get_tokens(line)))
		except:
			continue
		new_line = ''
		for tok in stem_clean_toks:
			new_line += tok + ' '
		outfile.write(new_line + '\n')

def simp_tokenizer(text):
	from nltk import word_tokenize
	
	return word_tokenize(text)

def make_corpus(path):
	from glob import glob
	files = glob(path)

	for doc in files:
		lines = open(doc, 'r').readlines()
		for line in lines:
			yield line

def tfidf(path):
	
	from sklearn.feature_extraction.text import TfidfVectorizer
	#from pdb import set_trace

	corpus = make_corpus(path = path)
	tfidf = TfidfVectorizer(max_features = 500, min_df = 0.2, use_idf = True, tokenizer = simp_tokenizer, analyzer = 'word', ngram_range = (1,1))
	#set_trace()
	tfs = tfidf.fit_transform(corpus)
	return tfs

def gensim_tfidf(path):
	from gensim import corpora, models, similarities
	from re import split
	from pdb import set_trace

	set_trace()
	corpus = make_corpus(path)
	docs = list()
	for doc in corpus:
		docs.append(split(' |\n', doc))
	del corpus
	dictionary = corpora.Dictionary(docs)
	dictionary.save('../fixtures/tmp/docs_small.dict')
	raw_docs = [dictionary.doc2bow(d) for d in docs]
	corpora.MmCorpus.serialize('../fixtures/tmp/docs_small.mm', raw_docs)
	del docs
	del raw_docs

	corpus = corpora.MmCorpus('../fixtures/tmp/docs_small.mm')
	tfidf = models.TfidfModel(corpus)
	index = similarities.MatrixSimilarity(tfidf[corpus])
	index.save('../fixtures/tmp/docs_small.index')
	sims = index[tfidf[corpus]]
	return sims

def build_weighted_corpora():
	"""
	"""
	from json import loads
	from csv import DictWriter
	from tqdm import tqdm

	doc_m = loads(open('../fixtures/tmp/corpora_doc2.corp', 'r').read())
	doc_f = loads(open('../fixtures/tmp/corpora_doc1.corp', 'r').read())
	dictionary = loads(open('../fixtures/tmp/corpora.dict', 'r').read())

	csvfile = open('../fixtures/all_csv/male_corpora.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in tqdm(doc_m):
		ix = tag[0]
		word = dictionary[ix]
		weight = tag[1]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = '0000ff'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

	csvfile = open('../fixtures/all_csv/female_corpora.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in tqdm(doc_f):
		ix = tag[0]
		word = dictionary[ix]
		weight = tag[1]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = 'ff0000'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

def build_weighted_corpora_exclude_same_ranks():
	"""
	"""
	from json import loads
	from csv import DictWriter
	from tqdm import tqdm
	from pdb import set_trace
	set_trace()
	doc_m = loads(open('../fixtures/tmp/corpora_doc2.corp', 'r').read())
	doc_f = loads(open('../fixtures/tmp/corpora_doc1.corp', 'r').read())
	dictionary = loads(open('../fixtures/tmp/corpora.dict', 'r').read())

	# Sort both lists by 2nd value
	temp_sorted_doc_m = sorted(doc_m, key = lambda x : x[1], reverse = True)
	temp_sorted_doc_f = sorted(doc_f, key = lambda x : x[1], reverse = True)

	# Remove null strings
	temp2_sorted_doc_m = list()
	temp2_sorted_doc_f = list()

	for tag in temp_sorted_doc_m:
		if dictionary[tag[0]] == '' or dictionary[tag[0]] == ' ':
			continue
		else:
			temp2_sorted_doc_m.append(tag)

	for tag in temp_sorted_doc_f:
		if dictionary[tag[0]] == '' or dictionary[tag[0]] == ' ':
			continue
		else:
			temp2_sorted_doc_f.append(tag)

	del temp_sorted_doc_m
	del temp_sorted_doc_f

	# Remove similarly ranked items
	sorted_doc_m = list()
	sorted_doc_f = list()

	for i in range(min(len(temp2_sorted_doc_m), len(temp2_sorted_doc_f))):
		if temp2_sorted_doc_m[i][0] == temp2_sorted_doc_f[i][0]:
			print temp2_sorted_doc_m[i]
			continue
		else:
			sorted_doc_m.append(temp2_sorted_doc_m[i])
			sorted_doc_f.append(temp2_sorted_doc_f[i])

	if len(temp2_sorted_doc_m) > len(temp2_sorted_doc_f):
		sorted_doc_m.extend(temp2_sorted_doc_m[i + 1:])
	elif len(temp2_sorted_doc_m) < len(temp2_sorted_doc_f):
		sorted_doc_f.extend(temp2_sorted_doc_f[i + 1:])
	else:
		pass

	del temp2_sorted_doc_m
	del temp2_sorted_doc_f

	csvfile = open('../fixtures/all_csv/male_corpora_no_same_rank.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in tqdm(sorted_doc_m):
		ix = tag[0]
		word = dictionary[ix]
		weight = tag[1]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = '0000ff'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

	csvfile = open('../fixtures/all_csv/female_corpora_no_same_rank.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in tqdm(sorted_doc_f):
		ix = tag[0]
		word = dictionary[ix]
		weight = tag[1]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = 'ff0000'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

def build_weighted_corpora_uncommon_words():
	"""
	"""
	from json import loads
	from csv import DictWriter
	from tqdm import tqdm
	from pdb import set_trace

	set_trace()
	doc_m = loads(open('../fixtures/tmp/corpora_doc2.corp', 'r').read())
	doc_f = loads(open('../fixtures/tmp/corpora_doc1.corp', 'r').read())
	dictionary = loads(open('../fixtures/tmp/corpora.dict', 'r').read())	

	my_special_dict_m = dict()
	my_special_dict_f = dict()

	only_tags_m = list()
	only_tags_f = list()

	for tag in doc_m: 
		my_special_dict_m[tag[0]] = tag[1]
		only_tags_m.append(tag[0])

	for tag in doc_f: 
		my_special_dict_f[tag[0]] = tag[1]
		only_tags_f.append(tag[0])

	uncommon_m = list(set(only_tags_m).difference(set(only_tags_f)))
	uncommon_f = list(set(only_tags_f).difference(set(only_tags_m)))

	csvfile = open('../fixtures/all_csv/male_corpora_uncommon.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in uncommon_m:
		word = dictionary[tag]
		weight = my_special_dict_m[tag]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = '0000ff'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

	csvfile = open('../fixtures/all_csv/female_corpora_uncommon.csv', 'w')
	fieldnames = ['Word', 'Weight', 'Color', 'Angle', 'Font', 'Repeat?']
	file_writer = DictWriter(csvfile, fieldnames = fieldnames, delimiter=';')
	file_writer.writeheader()
	for tag in uncommon_f:
		word = dictionary[tag]
		weight = my_special_dict_f[tag]
		tag_dict = dict()
		tag_dict['Word'] = word
		tag_dict['Weight'] = weight
		tag_dict['Color'] = 'ff0000'
		tag_dict['Angle'] = 0
		tag_dict['Font'] = 'PT Sans Regular'
		tag_dict['Repeat?'] = 0
		file_writer.writerow(tag_dict)
	csvfile.close()

def strip_punctuation(text):
	"""
	From Stack Overflow http://stackoverflow.com/questions/11066400/remove-punctuation-from-unicode-formatted-strings?lq=1
	"""
	from unicodedata import category
	punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
	return ''.join(x for x in text if category(x) not in punctutation_cats)


def get_bigrams(comment_list):
	"""
	Strip punctuations and generate bigrams with vaderSentiment
	"""

	bigrams = list()
	for comment in comment_list:
		no_punc_comment = strip_punctuation(comment)
		tokens = no_punc_comment.encode('utf-8').split()
		comment_bigrams = zip(tokens, tokens[1:])
		bigrams.extend(comment_bigrams)

	return bigrams

def get_bigram_sentiment_distribution(bigrams):
	"""
	Send the number of ([positive, neutral, negative], [positive, neutral, negative]) sentiment bigrams
	"""
	from vaderSentiment.vaderSentiment import sentiment
	from operator import itemgetter
	
	pos_pos = 0
	pos_neu = 0
	pos_neg = 0
	neu_pos = 0
	neu_neu = 0
	neu_neg = 0
	neg_pos = 0
	neg_neu = 0
	neg_neg = 0

	for tup in bigrams:
		word_one, word_two = tup
		vs_one = sentiment(word_one)
		del vs_one['compound']
		sent_one = sorted(vs_one.items(), key = itemgetter(1), reverse = True)[0][0]
		vs_two = sentiment(word_two)
		del vs_two['compound']
		sent_two = sorted(vs_two.items(), key = itemgetter(1), reverse = True)[0][0]

		if sent_one == 'pos':
			if sent_two == 'pos':
				pos_pos += 1
			elif sent_two == 'neu':
				pos_neu += 1
			else:
				pos_neg += 1
		elif sent_one == 'neu':
			if sent_two == 'pos':
				neu_pos += 1
			elif sent_two == 'neu':
				neu_neu += 1
			else:
				neu_neg += 1
		else:
			if sent_two == 'pos':
				neg_pos += 1
			elif sent_two == 'neu':
				neg_neu += 1
			else:
				neg_neg += 1

	return (pos_pos, pos_neu, pos_neg, neu_pos, neu_neu, neu_neg, neg_pos, neg_neu, neg_neg)

def get_punctuation_features(text):
	"""
	"""
	QUOTATION = '&quot;'
	PAUSES = [',', ';', ':']
	QUESTION = '?'
	EXCLAMATION = '!'

	num_quotes = text.count(QUOTATION)
	num_commas = text.count(PAUSES[0])
	num_semicolons = text.count(PAUSES[1])
	num_colons = text.count(PAUSES[2])
	num_pauses = num_colons + num_semicolons + num_commas
	num_questions = text.count(QUESTION)
	num_exclamations = text.count(EXCLAMATION)

	return {'num_quotes': num_quotes, 
			'num_commas': num_commas, 
			'num_semicolons': num_semicolons, 
			'num_colons': num_colons, 
			'num_pauses': num_pauses, 
			'num_questions': num_questions, 
			'num_exclamations': num_exclamations}

def get_pos_features(text):
	"""
	"""
	from nltk.tag import pos_tag, map_tag
	from nltk import word_tokenize

	toks = word_tokenize(text)
	posTagged = pos_tag(toks)
	simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
	tagset_dict = dict()

	for tup in simplifiedTags:
		tag = tup[1]
		if tag in tagset_dict:
			tagset_dict[tag] += 1
		else:
			tagset_dict[tag] = 1

	return tagset_dict

def get_general_text_features(text):
	"""
	"""
	from nltk import word_tokenize

	QUOTATION = '&quot;'
	PAUSES = [',', ';', ':']
	QUESTION = '?'
	EXCLAMATION = '!'
	OTHERS = ['(', ')', '[', ']', "'", '-', '{', '}', '.', '...']

	text = text.replace(QUOTATION, '')
	temptoks = word_tokenize(text)
	toks = list()
	for tok in temptoks:
		if tok in PAUSES or tok in OTHERS:
			continue
		elif tok == QUESTION or tok == EXCLAMATION:
			continue
		else:
			toks.append(tok)

	num_unq_words = len(list(set(toks)))
	return {'num_unq_words': num_unq_words}

def get_word_vector(text):
	"""
	"""
	from operator import itemgetter
	from string import punctuation

	exclude = set(punctuation)
	no_punc_text = ''.join(ch for ch in text if ch not in exclude)
	no_punc_text = no_punc_text.lower()
	text_tokens = no_punc_text.split()
	filtered_tokens = remove_stopwords(text_tokens)
	wc_vector = get_word_count(filtered_tokens)
	final_vector = wc_vector.most_common(200)
	return final_vector

















#if __name__ == '__main__':
#	main()