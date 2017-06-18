#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import re
from urllib import request

# Import external packages
from bs4 import BeautifulSoup
import bs4
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

# def get_HTMLdoc(url):
# 	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
# 	req = request.Request(url, headers=headers)
# 	req = request.urlopen(req)
	
# 	charset = req.info().get_content_charset()
# 	# self.doc = req.read().decode(charset)
# 	doc = req.read().decode(charset)

# 	soup = BeautifulSoup(doc, "html.parser")
# 	return soup

def encode_xpath(xpath, seq_tagcode, range_xpath):
	xpath_encoded_tagname = np.zeros(shape=(range_xpath), dtype=np.int32)
	xpath_encoded_occurence = np.zeros(shape=(range_xpath), dtype=np.int32)
	seq_elem = xpath.split("/")
	
	for i in range(0, len(seq_elem)-1, 2):
		try:
			index = int(i/2)
			xpath_encoded_tagname[index] = SEQ_TAGCODE.index(seq_elem[i])
			xpath_encoded_occurence[index] = int(seq_elem[i+1])
		except ValueError: # Trivial error not so important for now
			pass

	return xpath_encoded_tagname, xpath_encoded_occurence

class XpathFinder():
	def __init__(self, url):
		# Caches
		self.__path_prev = ""
		self.__stack_path_prev = []

		# Values potentially to return
		self.soup = None
		self.seq_xpath = []
		self.shape_seq_xpath = ()
		self.seq_xpath_encoded = []
		self.uniqseq_xpath_encoded = []
		self.seq_xpath_encoded_occurence = []
		self.seq_map_xpath = []

		# Initial actions upon instantiation
		self.get_HTMLdoc(url)
		
		self.run_make_seq_xpath()
		self.filter_seq_xpath()

		self.make_shape_seq_xpath()
		self.make_seq_xpath_encoded()
		self.make_uniqseq_xpath_encoded()
		self.make_seq_xpath_encoded_sparse()

	def refine_doc(self, doc):
		pass

	def get_HTMLdoc(self, url):
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
		
		req = request.Request(url, headers=headers)
		req = request.urlopen(req)
		
		charset = req.info().get_content_charset()
		doc = req.read().decode(charset)

		soup = BeautifulSoup(doc, "html.parser")
		# [s.decompose() for s in soup('span')]
		# [s.decompose() for s in soup('p')]
		# [s.decompose() for s in soup('em')]
		# [s.decompose() for s in soup('strong')]
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('style')]
		self.soup = soup
		# return soup

	def run_make_seq_xpath(self):
		# Becasue make_seq_xpath is a recursive action
		self.make_seq_xpath(self.get_soup())
	
	def make_seq_xpath(self, elem):
		list_tmp = []
		for child in elem.children:
			count = list_tmp.count(child.name)
			list_tmp.append(child.name)

			if type(child) == bs4.element.Tag:
				self.__stack_path_prev.append(self.__path_prev)
				self.__path_prev = self.__path_prev + str(child.name) + "/{0}".format(count) + "/"
				
				self.make_seq_xpath(child)
				self.__path_prev = self.__stack_path_prev.pop()

			elif type(child) == bs4.element.NavigableString:
				self.seq_xpath.append(self.__path_prev.lstrip("/")) # + str(child.name) + "/{0}".format(count) + "/")

	def filter_seq_xpath(self):
		# Set operation doesn't preserve the order
		seq_xpath_filtered_once = []
		for xpath in self.seq_xpath:
			if xpath not in seq_xpath_filtered_once:
				seq_xpath_filtered_once.append(xpath)

		seq_xpath_filtered_twice = []
		for xpath in seq_xpath_filtered_once:
			if re.search(r"script|style", xpath) == None:
				seq_xpath_filtered_twice.append(xpath)

		self.seq_xpath = seq_xpath_filtered_twice

	def make_shape_seq_xpath(self):
		seq_depth = [len(xpath.split("/")) for xpath in self.seq_xpath]
		self.shape_seq_xpath = (len(self.seq_xpath), max(seq_depth)//2)

	def make_seq_xpath_encoded(self):
		shape = self.shape_seq_xpath
		self.seq_xpath_encoded = np.zeros(shape=shape, dtype=np.int32)
		self.seq_xpath_encoded_occurence = np.zeros(shape=shape, dtype=np.int32)
		
		for i, xpath in enumerate(self.seq_xpath):
			self.seq_xpath_encoded[i] = encode_xpath(xpath, SEQ_TAGCODE, shape[1])[0]
			self.seq_xpath_encoded_occurence[i] = encode_xpath(xpath, SEQ_TAGCODE, shape[1])[1]

	def make_uniqseq_xpath_encoded(self):
		self.uniqseq_xpath_encoded = np.vstack({tuple(row) for row in self.seq_xpath_encoded})
		

	def make_seq_xpath_encoded_sparse(self):
		shape = self.shape_seq_xpath
		self.seq_xpath_encoded_sparse = np.zeros(shape=(shape[0], shape[1], len(SEQ_TAGCODE)), dtype=np.int32)
		for i, xpath_encoded in enumerate(self.get_seq_xpath_encoded()):
			for j, code in enumerate(xpath_encoded):
				self.seq_xpath_encoded_sparse[i, j, code] = 1

	# Inter
	def make_seq_map_xpath(self, intersect_xpath_encoded):
		seq_xpath_encoded = self.get_seq_xpath_encoded()
		
		seq_map_xpath = np.zeros(shape=(seq_xpath_encoded.shape[0], 2), dtype=np.int32)
		seq_map_xpath.fill(-1)
		
		index_mapped = 0
		for i, xpath_encoded in enumerate(seq_xpath_encoded):
			for j, xpath_encoded_uniq in enumerate(intersect_xpath_encoded):
				if np.array_equal(xpath_encoded, xpath_encoded_uniq):
					seq_map_xpath[i] = np.array([i, index_mapped], dtype=np.int32)
					index_mapped += 1
		seq_map_xpath = seq_map_xpath[~np.all(seq_map_xpath == -1, axis=1)]
		
		self.seq_map_xpath = seq_map_xpath

	# Inter
	def make_shrunkseq_xpath_encoded(self):
		seq_map_xpath = self.get_seq_map_xpath()
		seq_xpath_encoded = self.get_seq_xpath_encoded()

		shrunkseq_xpath_encoded = np.zeros(shape=(seq_map_xpath.shape[0], seq_xpath_encoded.shape[1]), dtype=np.int32)
		for map_xpath in seq_map_xpath:
			shrunkseq_xpath_encoded[map_xpath[1]] = seq_xpath_encoded[map_xpath[0]]

		self.shrunkseq_xpath_encoded = shrunkseq_xpath_encoded
		# return shrunkseq_xpath_encoded

	# Getters
	def get_soup(self):
		return self.soup

	def get_seq_xpath(self):
		return self.seq_xpath

	def get_seq_xpath_encoded_occurence(self):
		return self.seq_xpath_encoded_occurence

	def get_seq_xpath_encoded(self):
		return self.seq_xpath_encoded

	def get_uniqseq_xpath_encoded(self):
		return self.uniqseq_xpath_encoded

	def get_seq_xpath_encoded_sparse(self):
		return self.seq_xpath_encoded_sparse
	
	def get_shape_seq_xpath(self):
		return self.shape_seq_xpath

	def get_seq_map_xpath(self):
		return self.seq_map_xpath

	def get_shrunkseq_xpath_encoded(self):
		return self.shrunkseq_xpath_encoded



# Possibly deprecated
# def get_HTMLdoc(url):
# 	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
# 	req = request.Request(url, headers=headers)
# 	req = request.urlopen(req)
	
# 	charset = req.info().get_content_charset()
# 	ret = req.read().decode(charset)
# 	return ret

# def get_list_xpath(doc, tags_ignored, path_prev="", ret=[]):
# 	list_tmp = []
# 	# ret.append(path_prev.lstrip("/"))
# 	for child in doc.children:
# 		count = list_tmp.count(child.name)
# 		list_tmp.append(child.name)
		
# 		# if isin_irrelevant_tag(child, tags_ignored) == True:
# 		# 	if count == 0 and child.name in ["p"]:
# 		# 		# print(path_prev.lstrip("/") + "/"+ child.name + ":{0}".format(count) + "/")
# 		# 		ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
# 		if hasattr(child, "children") == True and len(list(child.children)) < 2:			
# 			ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
# 		elif hasattr(child, "children") == True:
# 			get_list_xpath(child, tags_ignored, path_prev + "/"+ child.name + "/{0}".format(count), ret)
# 	return ret

# def get_range_xpath(seq_xpath):
# 	"""
# 	Get the (rendered) maximum depth of xpaths
# 	"""
# 	seq_depth = [len(xpath.split("/")) for xpath in seq_xpath]
# 	depth_max = max(seq_depth)//2
# 	return depth_max


