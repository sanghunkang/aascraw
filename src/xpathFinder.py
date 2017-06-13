#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
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
	# xpath_encoded = np.zeros(shape=(2, range_xpath), dtype=np.int32)
	xpath_encoded = np.zeros(shape=(range_xpath), dtype=np.int32)
	seq_elem = xpath.split("/")
	
	for i in range(0, len(seq_elem)-1, 2):
		try:
			index = int(i/2)
			xpath_encoded[index] = SEQ_TAGCODE.index(seq_elem[i])
			# xpath_encoded[0, index] = SEQ_TAGCODE.index(seq_elem[i])
			# xpath_encoded[1, index] = int(seq_elem[i+1])
		except ValueError: # Trivial error not so important for now
			pass

	return xpath_encoded

class XpathFinder():
	def __init__(self, url):
		# Caches
		self.__path_prev = ""
		self.__stack_path_prev = []

		# Values potentially to return
		self.soup = None
		self.seq_xpath = []
		self.shape_seq_xpath = ()
		self.seq_xpath_encoded_2d = []

		# Initial actions upon instantiation
		self.get_HTMLdoc(url)
		self.make_seq_xpath(self.soup)
		self.make_shape_seq_xpath()
		self.make_seq_xpath_encoded_2d()
		self.make_seq_xpath_encoded_3d()

	def get_HTMLdoc(self, url):
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
		
		req = request.Request(url, headers=headers)
		req = request.urlopen(req)
		
		charset = req.info().get_content_charset()
		doc = req.read().decode(charset)

		self.soup = BeautifulSoup(doc, "html.parser")
		# return soup

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

	def make_shape_seq_xpath(self):
		seq_depth = [len(xpath.split("/")) for xpath in self.seq_xpath]
		self.shape_seq_xpath = (len(self.seq_xpath), max(seq_depth)//2)

	def make_seq_xpath_encoded_2d(self):
		shape = self.shape_seq_xpath
		self.seq_xpath_encoded_2d = np.zeros(shape=shape, dtype=np.int32)
		
		for i, xpath in enumerate(self.seq_xpath):
			self.seq_xpath_encoded_2d[i] = encode_xpath(xpath, SEQ_TAGCODE, shape[1])

	def make_seq_xpath_encoded_3d(self):
		shape = self.shape_seq_xpath
		self.seq_xpath_encoded_3d = np.zeros(shape=(shape[0], shape[1], len(SEQ_TAGCODE)), dtype=np.int32)
		for i, xpath_encoded in enumerate(self.get_seq_xpath_encoded_2d()):
			for j, code in enumerate(xpath_encoded):
				self.seq_xpath_encoded_3d[i, j, code] = 1

	# Getters
	def get_seq_xpath(self):
		return self.seq_xpath

	def get_seq_xpath_encoded_2d(self):
		return self.seq_xpath_encoded_2d

	def get_seq_xpath_encoded_3d(self):
		return self.seq_xpath_encoded_3d
	
	def get_shape_seq_xpath(self):
		return self.shape_seq_xpath




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


