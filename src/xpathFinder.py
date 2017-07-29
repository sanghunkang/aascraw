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
	def __init__(self, seq_tag_unwrap=SEQ_TAG_UNWRAP, seq_tag_decomp=SEQ_TAG_DECOMP):
		self.seq_tag_unwrap = seq_tag_unwrap
		self.seq_tag_decomp = seq_tag_decomp

	def render_soup(self, soup):
		"""
		Function to unwrap or remove unnecessary tags, - plus their contents, 
		most of which are decorative - since decorative tags worsen outputs. 
		Defaults are chosen emprically. Comments are always removed.
		
		args:
			soup 		: bs4.BeautifulSoup, directly from page source
		return:
			soup 		: bs4.BeautifulSoup, with annoying part removed
		"""
		seq_text_comment = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))

		for comment in seq_text_comment: comment.extract()
		for tag_unwrap in self.seq_tag_unwrap: [s.unwrap() for s in soup(tag_unwrap)]
		for tag_decomp in self.seq_tag_decomp: [s.decompose() for s in soup(tag_decomp)]
		
		return soup

	def receive_soup(self, soup):
		self.cmd_driver = "cmd control here"
		return self.render_soup(soup)

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
		return self.render_soup(soup)

	def generate_soup(self, arg):
		assert isinstance(arg, str) or isinstance(arg, bs4.BeautifulSoup)

		if isinstance(arg, str): soup = self.receive_url(arg)
		else: soup = self.receive_soup(arg)
		
		print(soup)
		return soup

	def encode_xpath(self, xpath, seq_tagcode, range_xpath):
		xpath_encoded_tagname = np.zeros(shape=(range_xpath), dtype=np.int32)
		xpath_encoded_occurence = np.zeros(shape=(range_xpath), dtype=np.int32)
		seq_elem = xpath.split("/")
		
		for i in range(0, len(seq_elem)-1, 2):
			try:
				index = int(i/2)
				xpath_encoded_tagname[index] = SEQ_TAGCODE.index(seq_elem[i])
				xpath_encoded_occurence[index] = int(seq_elem[i+1])
			except ValueError: # Trivial error, not so important for now
				pass

		return xpath_encoded_tagname, xpath_encoded_occurence
	
	
	def make_shape_seq_xpath(self, seq_xpath):
		seq_depth = [len(xpath.split("/")) for xpath in seq_xpath]
		# self.shape_seq_xpath = (len(self.seq_xpath), max(seq_depth)//2)
		shape_seq_xpath = (len(seq_xpath), max(seq_depth)//2)
		return shape_seq_xpath

	def make_seq_xpath(self, elem):
		seq_xpath = []
		list_tmp = []
		for child in elem.children:
			count = list_tmp.count(child.name)
			list_tmp.append(child.name)

			if type(child) == bs4.element.Tag:
				self.__stack_path_prev.append(self.__path_prev)
				self.__path_prev = "{0}{1}/{2}/".format(self.__path_prev, str(child.name), count)
				
				seq_xpath = seq_xpath + self.make_seq_xpath(child)
				self.__path_prev = self.__stack_path_prev.pop()

			elif type(child) == bs4.element.NavigableString:
				seq_xpath.append(self.__path_prev.lstrip("/"))
		return seq_xpath

	def filter_seq_xpath(self, seq_xpath):
		seq_xpath_filtered = []
		for xpath in seq_xpath:
			if xpath not in seq_xpath_filtered and len(xpath) > 1:
				seq_xpath_filtered.append(xpath)

		return seq_xpath_filtered

	def make_seq_xpath_encoded(self, shape, seq_xpath):
		seq_xpath_encoded = np.zeros(shape=shape, dtype=np.int32)
		for i, xpath in enumerate(seq_xpath): seq_xpath_encoded[i] = self.encode_xpath(xpath, SEQ_TAGCODE, shape[1])[0]
		# self.seq_xpath_encoded_occurence[i] = self.encode_xpath(xpath, SEQ_TAGCODE, shape[1])[1]
		return seq_xpath_encoded


	def initialize_cache(self):
		# Caches
		self.__path_prev = ""
		self.__stack_path_prev = []
		self.cmd_driver = None

	def generate_seq_xpath(self, soup):
		seq_xpath = self.make_seq_xpath(soup)
		seq_xpath_filtered = self.filter_seq_xpath(seq_xpath)
		return seq_xpath_filtered

	def generate_uniqseq_xpath_encoded(self, seq_xpath):
		shape_seq_xpath = self.make_shape_seq_xpath(seq_xpath)
		seq_xpath_encoded = self.make_seq_xpath_encoded(shape_seq_xpath, seq_xpath)
		return np.vstack({tuple(row) for row in seq_xpath_encoded})

	def extract_pageinfo(self, arg):
		self.initialize_cache()

		soup = self.generate_soup(arg)
		seq_xpath = self.generate_seq_xpath(soup)
		uniqseq_xpath_encoded = self.generate_uniqseq_xpath_encoded(seq_xpath)

		return Pageinfo(soup, seq_xpath, uniqseq_xpath_encoded)

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