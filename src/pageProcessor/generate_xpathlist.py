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

class XpathFinder():
	def __init__(self):		
		self.path_prev = ""
		self.seq_xpath = []
		self.stack_path_prev = []
		
	def make_seq_xpath(self, elem):
		list_tmp = []
		for child in elem.children:
			count = list_tmp.count(child.name)
			list_tmp.append(child.name)

			if type(child) == bs4.element.Tag:
				self.stack_path_prev.append(self.path_prev)
				self.path_prev = self.path_prev + str(child.name) + "/{0}".format(count) + "/"
				
				self.make_seq_xpath(child)
				self.path_prev = self.stack_path_prev.pop()

			elif type(child) == bs4.element.NavigableString:
				self.seq_xpath.append(self.path_prev.lstrip("/")) # + str(child.name) + "/{0}".format(count) + "/")

		return self.seq_xpath

def get_HTMLdoc(url):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
	req = request.Request(url, headers=headers)
	req = request.urlopen(req)
	
	charset = req.info().get_content_charset()
	ret = req.read().decode(charset)
	return ret

def isin_irrelevant_tag(child, tags_ignored):
	if child.name in tags_ignored:
		ret = True
	else:
		ret = False
	return ret

# Possibly deprecated
def get_list_xpath(doc, tags_ignored, path_prev="", ret=[]):
	list_tmp = []
	# ret.append(path_prev.lstrip("/"))
	for child in doc.children:
		count = list_tmp.count(child.name)
		list_tmp.append(child.name)
		
		# if isin_irrelevant_tag(child, tags_ignored) == True:
		# 	if count == 0 and child.name in ["p"]:
		# 		# print(path_prev.lstrip("/") + "/"+ child.name + ":{0}".format(count) + "/")
		# 		ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
		if hasattr(child, "children") == True and len(list(child.children)) < 2:			
			ret.append(path_prev.lstrip("/") + "/"+ child.name + "/{0}".format(count) + "/")
		elif hasattr(child, "children") == True:
			get_list_xpath(child, tags_ignored, path_prev + "/"+ child.name + "/{0}".format(count), ret)
	return ret


def get_range_xpath(seq_xpath):
	"""
	Get the (rendered) maximum depth of xpaths
	"""
	seq_depth = [len(xpath.split("/")) for xpath in seq_xpath]
	depth_max = max(seq_depth)//2
	return depth_max

