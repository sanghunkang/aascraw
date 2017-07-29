#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import re
from urllib import request

# Import external packages
import bs4
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

class Pageinfo():
	def __init__(self, soup, seq_xpath, uniqseq_xpath_encoded):
		self.soup = soup
		self.seq_xpath = seq_xpath
		self.uniqseq_xpath_encoded = uniqseq_xpath_encoded

	def get_soup(self):
		return self.soup

	def get_seq_xpath(self):
		return self.seq_xpath

	def get_uniqseq_xpath_encoded(self):
		return self.uniqseq_xpath_encoded

class XpathFinder():
	def __init__(self):
		# Caches
		self.__path_prev = ""
		self.__stack_path_prev = []

		# Values potentially to return
		self.cmd_driver = None
		self.soup = None
		self.seq_xpath = []
		self.shape_seq_xpath = ()
		self.seq_xpath_encoded = []
		self.uniqseq_xpath_encoded = []
		self.seq_xpath_encoded_occurence = []
		self.seq_map_xpath = []

		# Initial actions upon instantiation

	def render_soup(self, soup):
		"""
		Function to unwrap or remove unnecessary tags, - plus their contents, 
		most of which are decorative - since decorative tags worsen outputs. 
		Defaults are chosen emprically. Comments are always removed.
		
		args:

		"""
		seq_text_comment = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
		for comment in seq_text_comment: comment.extract()

		seq_tag_unwrap = ["br","span","p","em","img","strong"]
		seq_tag_decomp = ["a","script","style"]
		for tag_unwrap in seq_tag_unwrap: [s.unwrap() for s in soup(tag_unwrap)]
		for tag_decomp in seq_tag_decomp: [s.decompose() for s in soup(tag_decomp)]

		return soup

	def receive_soup(self, soup):
		soup = self.render_soup(soup)
		print(soup)
		self.cmd_driver = "cmd control here"
		self.soup = soup

	def receive_url(self, url):
		"""

		"""
		# Please note that some websites don't allow automated scraping.
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
		
		req = request.Request(url, headers=headers)
		req = request.urlopen(req)
		
		charset = req.info().get_content_charset()
		doc = req.read().decode(charset)

		soup = bs4.BeautifulSoup(doc, "html.parser")
		self.receive_soup(soup)

	def run_make_seq_xpath(self, arg):
		# Caches
		self.__path_prev = ""
		self.__stack_path_prev = []

		# Values potentially to return
		self.cmd_driver = None
		self.soup = None
		self.seq_xpath = []
		self.shape_seq_xpath = ()
		self.seq_xpath_encoded = []
		self.uniqseq_xpath_encoded = []
		self.seq_xpath_encoded_occurence = []
		self.seq_map_xpath = []

		if isinstance(arg, str): self.receive_url(arg)
		elif isinstance(arg, bs4.BeautifulSoup): self.receive_soup(arg)

		# Becasue make_seq_xpath is a recursive action
		self.make_seq_xpath(self.get_soup())
		self.filter_seq_xpath()

		self.make_shape_seq_xpath()

		self.make_seq_xpath_encoded()
		self.make_uniqseq_xpath_encoded()

		# self.make_seq_xpath_encoded_sparse()

	

	def encode_xpath(self, xpath, seq_tagcode, range_xpath):
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
		# Note: Set operation doesn't preserve the order
		seq_xpath_filtered = []
		for xpath in self.seq_xpath:
			if xpath not in seq_xpath_filtered and len(xpath) > 1:
				seq_xpath_filtered.append(xpath)

		self.seq_xpath = seq_xpath_filtered

	def make_shape_seq_xpath(self):
		seq_depth = [len(xpath.split("/")) for xpath in self.seq_xpath]
		self.shape_seq_xpath = (len(self.seq_xpath), max(seq_depth)//2)

	def make_seq_xpath_encoded(self):
		shape = self.shape_seq_xpath
		self.seq_xpath_encoded = np.zeros(shape=shape, dtype=np.int32)
		self.seq_xpath_encoded_occurence = np.zeros(shape=shape, dtype=np.int32)
		
		for i, xpath in enumerate(self.seq_xpath):
			self.seq_xpath_encoded[i] = self.encode_xpath(xpath, SEQ_TAGCODE, shape[1])[0]
			self.seq_xpath_encoded_occurence[i] = self.encode_xpath(xpath, SEQ_TAGCODE, shape[1])[1]

	def make_uniqseq_xpath_encoded(self):
		seq_xpath_encoded = self.get_seq_xpath_encoded()
		self.uniqseq_xpath_encoded = np.vstack({tuple(row) for row in seq_xpath_encoded})
	
	def extract_pageinfo(self, arg):
		self.run_make_seq_xpath(arg)
		soup = self.get_soup()
		seq_xpath = self.get_seq_xpath()
		uniqseq_xpath_encoded = self.get_uniqseq_xpath_encoded()

		pagainfo = Pageinfo(soup, seq_xpath, uniqseq_xpath_encoded)
		return pagainfo

	# def make_seq_xpath_encoded_sparse(self):
	# 	shape = self.shape_seq_xpath
	# 	self.seq_xpath_encoded_sparse = np.zeros(shape=(shape[0], shape[1], len(SEQ_TAGCODE)), dtype=np.int32)
	# 	for i, xpath_encoded in enumerate(self.get_seq_xpath_encoded()):
	# 		for j, code in enumerate(xpath_encoded):
	# 			self.seq_xpath_encoded_sparse[i, j, code] = 1

	# Inter
	# def make_seq_map_xpath(self, intersect_xpath_encoded):
	# 	seq_xpath_encoded = self.get_seq_xpath_encoded()
		
	# 	seq_map_xpath = np.zeros(shape=(seq_xpath_encoded.shape[0], 2), dtype=np.int32)
	# 	seq_map_xpath.fill(-1)
		
	# 	index_mapped = 0
	# 	for i, xpath_encoded in enumerate(seq_xpath_encoded):
	# 		for j, xpath_encoded_uniq in enumerate(intersect_xpath_encoded):
	# 			if np.array_equal(xpath_encoded, xpath_encoded_uniq):
	# 				seq_map_xpath[i] = np.array([i, index_mapped], dtype=np.int32)
	# 				index_mapped += 1
	# 	seq_map_xpath = seq_map_xpath[~np.all(seq_map_xpath == -1, axis=1)]
		
	# 	self.seq_map_xpath = seq_map_xpath

	# def make_shrunkseq_xpath_encoded(self):
	# 	seq_map_xpath = self.get_seq_map_xpath()
	# 	seq_xpath_encoded = self.get_seq_xpath_encoded()

	# 	shrunkseq_xpath_encoded = np.zeros(shape=(seq_map_xpath.shape[0], seq_xpath_encoded.shape[1]), dtype=np.int32)
	# 	for map_xpath in seq_map_xpath:
	# 		shrunkseq_xpath_encoded[map_xpath[1]] = seq_xpath_encoded[map_xpath[0]]

	# 	self.shrunkseq_xpath_encoded = shrunkseq_xpath_encoded
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

	# def get_seq_xpath_encoded_sparse(self):
	# 	return self.seq_xpath_encoded_sparse
	
	def get_shape_seq_xpath(self):
		return self.shape_seq_xpath

	# def get_seq_map_xpath(self):
	# 	return self.seq_map_xpath

	# def get_shrunkseq_xpath_encoded(self):
	# 	return self.shrunkseq_xpath_encoded