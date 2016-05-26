#!/usr/bin/env python

def get_attributes(doc):
	"""
	Gets the attribute list for passed document
	"""
	return doc.keys()

def cursor_nelements(cursor):
	"""
	Returns the number of elements in the passed cursor
	"""
	count = 0
	for data in cursor:
		count += 1
	return count

def get_id(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor IDs
	"""
	if cursor is None and doc is not None:
		return doc['id']
	elif doc is None and cursor is not None:
		allids = list()
		for thisdoc in cursor:
			allids.append(thisdoc['id'])
		return allids
	else:
		print "Supply any one argument only!"

def get_name(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor names
	"""
	if cursor is None and doc is not None:
		return doc['name']
	elif doc is None and cursor is not None:
		allnames = list()
		for thisdoc in cursor:
			allnames.append(thisdoc['name'])
		return allnames
	else:
		print "Supply any one argument only!"

def get_emb_details(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's embedded details documents
	"""
	if cursor is None and doc is not None:
		return doc['details']
	elif doc is None and cursor is not None:
		allrats = list()
		for thisdoc in cursor:
			allrats.append(thisdoc['details'])
		return allrats
	else:
		print "Supply any one argument only!"

def get_emb_ratings(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's embedded rating documents
	"""
	if cursor is None and doc is not None:
		return doc['ratings']
	elif doc is None and cursor is not None:
		allrats = list()
		for thisdoc in cursor:
			allrats.append(thisdoc['ratings'])
		return allrats
	else:
		print "Supply any one argument only!"

def get_emb_comments(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's embedded comment documents 
	"""
	if cursor is None and doc is not None:
		return doc['all comments']
	elif doc is None and cursor is not None:
		allcoms = list()
		for thisdoc in cursor:
			allcoms.append(thisdoc['all comments'])
		return allcoms
	else:
		print "Supply any one argument only!"

def get_university(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's university 
	"""
	if cursor is None and doc is not None:
		return doc['details']['university']
	elif doc is None and cursor is not None:
		allunivs = list()
		for thisdoc in cursor:
			allunivs.append(thisdoc['details']['university'])
		return allunivs
	else:
		print "Supply any one argument only!"

def get_state(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's state 
	"""
	if cursor is None and doc is not None:
		return doc['details']['state']
	elif doc is None and cursor is not None:
		allstates = list()
		for thisdoc in cursor:
			allstates.append(thisdoc['details']['state'])
		return allstates
	else:
		print "Supply any one argument only!"

def get_city(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's city 
	"""
	if cursor is None and doc is not None:
		return doc['details']['city']
	elif doc is None and cursor is not None:
		allcities = list()
		for thisdoc in cursor:
			allcities.append(thisdoc['details']['city'])
		return allcities
	else:
		print "Supply any one argument only!"

def get_university(doc = None, cursor = None):
	"""
	Takes a single document or a cursor of documents and returns the professor's university 
	"""
	if cursor is None and doc is not None:
		return doc['details']['university']
	elif doc is None and cursor is not None:
		allunivs = list()
		for thisdoc in cursor:
			allunivs.append(thisdoc['details']['university'])
		return allcoms
	else:
		print "Supply any one argument only!"


