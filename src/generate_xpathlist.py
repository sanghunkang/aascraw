#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from urllib import request

# Import external packages
from bs4 import BeautifulSoup
import numpy as np

def get_HTMLdoc(url):
	req = request.urlopen(url)
	charset = req.info().get_content_charset()
	ret = req.read().decode(charset)
	return ret

def isin_irrelevant_tag(child, tags_ignored):
	if child.name in tags_ignored:
		ret = True
	else:
		ret = False
	return ret

def get_list_xpath(doc, tags_ignored, path_prev="", ret=[]):
	list_tmp = []
	for child in doc.children:
		count = list_tmp.count(child.name)
		list_tmp.append(child.name)
		
		if isin_irrelevant_tag(child, tags_ignored) == True:
			if count == 0 and child.name in ["p"]:
				# print(path_prev.lstrip("/") + "/"+ child.name + ":{0}".format(count) + "/")
				ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
		if hasattr(child, "children") == True and len(list(child.children)) < 2:			
			ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
		elif hasattr(child, "children") == True:
			get_list_xpath(child, tags_ignored, path_prev + "/"+ child.name + "/{0}".format(count), ret)
	
	return ret

def encode_xpath(xpath, seq_tagcode, range_xpath):
	seq_tag_encoded = np.zeros(shape=(range_xpath))
	seq_occ_encoded = np.zeros(shape=(range_xpath))
	print(xpath)
	seq_elem = xpath.split("/")
	print(len(seq_elem))
	# print(seq_elem)
	for i in range(0, len(seq_elem)-1, 2):
		try:
			index = int(i/2)
			seq_tag_encoded[index] = seq_tagcode.index(seq_elem[i])
			seq_occ_encoded[index] = int(seq_elem[i+1])
		except ValueError: # Trivial error not so important for now
			pass
	 # = [seq_tagcode.index(elem) for i, elem in enumerate(xpath.split("/")[:-1]) if i%2 == 0]
	# seq_occ_encoded = [int(elem) for i, elem in enumerate(xpath.split("/")[:-1]) if i%2 == 1]
	xpath_encoded = np.concatenate([[seq_tag_encoded], [seq_occ_encoded]])
	return xpath_encoded