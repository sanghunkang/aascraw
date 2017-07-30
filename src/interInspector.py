#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from functools import reduce

# Import external packages
import numpy as np

# Import custom modules
# from driverController.locator import get_attr_elem, locate_element, get_eigentext
from driverController.locator import Locator

# Import package-wide constants
from constGlobal import *

class InterInspector():
	def __init__(self):
		self.seq_pageinfo = []
		self.intersect_xpath_encoded = []

	def receive_pageinfo(self, pageinfo):
		self.seq_pageinfo.append(pageinfo)

	def generate_seq_seq_xpath(self, seq_pageinfo):
		seq_seq_xpath = [pageinfo.get_seq_xpath() for pageinfo in seq_pageinfo]
		return seq_seq_xpath

	def generate_intersect_xpath(self, seq_pageinfo):
		seq_seq_xpath = self.generate_seq_seq_xpath(seq_pageinfo)
		intersect_xpath = list(set(seq_seq_xpath[0]).intersection(*seq_seq_xpath))
		intersect_xpath.sort(key=seq_seq_xpath[0].index)
		return intersect_xpath

	def generate_seq_locator(self, seq_pageinfo):
		seq_locator = [Locator(pageinfo) for pageinfo in seq_pageinfo]
		return seq_locator

	def generate_seq_eigentext(self, xpath, seq_locator):
		seq_eigentext = [locator.generate_eigentext(xpath) for locator in seq_locator]
		
		# Only for logging purpose
		if len(set(seq_eigentext)) > 1: 
			for eigentext in seq_eigentext:
				print(eigentext + "\n_______________________________________________________________")

		return seq_eigentext

	def generate_seq_xpath_canddt_inter(self):
		seq_pageinfo = self.get_seq_pageinfo()
		intersect_xpath = self.generate_intersect_xpath(seq_pageinfo)
		seq_locator = self.generate_seq_locator(seq_pageinfo)

		seq_xpath_canddt_inter = []
		for i, xpath in enumerate(intersect_xpath):
			print(i, "###########################################################################\n" + xpath)
			seq_eigentext = self.generate_seq_eigentext(xpath, seq_locator)			
			
			# If any difference among the seq is found
			if len(set(seq_eigentext)) > 1: seq_xpath_canddt_inter.append(xpath)
		return seq_xpath_canddt_inter

	# Getters ... well defined
	def get_seq_pageinfo(self):
		return self.seq_pageinfo

	def get_seq_xpath_canddt_inter(self):
		return self.seq_xpath_canddt_inter

# def make_map(seq_xpath_encoded, intersect_xpath_encoded):
# 	seq_map_xpath = np.zeros(shape=(seq_xpath_encoded.shape[0],2), dtype=np.int32)
# 	seq_map_xpath.fill(-1)
	
# 	index_mapped = 0
# 	for i, xpath_encoded in enumerate(seq_xpath_encoded):
# 		for j, xpath_encoded_unq in enumerate(intersect_xpath_encoded):
# 			if np.array_equal(xpath_encoded, xpath_encoded_unq):
# 				seq_map_xpath[i] = np.array([i, index_mapped], dtype=np.int32)
# 				index_mapped += 1
# 	seq_map_xpath = seq_map_xpath[~np.all(seq_map_xpath == -1, axis=1)]
# 	return seq_map_xpath

# possilbly skip this stage
"""
# def shrink1st_seq_xpath_encoded(seq_xpath_encoded, seq_map_xpath):
# 	shrunkseq_xpath_encoded = np.zeros(shape=(seq_map_xpath.shape[0], seq_xpath_encoded.shape[1]), dtype=np.int32)
# 	for map_xpath in seq_map_xpath:
# 		shrunkseq_xpath_encoded[map_xpath[1]] = seq_xpath_encoded[map_xpath[0]]
# 	return shrunkseq_xpath_encoded


# def simpleshrink(seq_xpath_target, seq_seq_xpath):
# 	# Doesn't seem perfect
# 	seq_xpath_simpleshrink = []
# 	for i, xpath in enumerate(seq_xpath_target):
# 		is_repeating = True
# 		for seq_xpath in seq_seq_xpath:
# 			if xpath not in seq_xpath:
# 				is_repeating == False
# 				break
# 		if is_repeating == True:
# 			print(xpath)
# 			seq_xpath_simpleshrink.append(xpath)
# 	return seq_xpath_simpleshrink

def shrink2nd_seq_xpath_encoded(seq_xpath_encoded_target, seq_xpath_encoded_compared):
	if len(seq_xpath_encoded_target) < len(seq_xpath_encoded_compared):
		sxe0, sxe1 = seq_xpath_encoded_target, seq_xpath_encoded_compared
	else:
		sxe0, sxe1 = seq_xpath_encoded_compared, seq_xpath_encoded_target

	map_sxe0, map_sxe1 = [], []
	i, fwdstep, backstep= 0, 0, 0
	while i < sxe0.shape[0]:
		try:		
			if np.array_equal(sxe0[i], sxe1[i+fwdstep+backstep]):
				map_sxe0.append(i)
				map_sxe1.append(i + fwdstep + backstep)
				i += 1
			else:
				fwdstep += 1
		except IndexError:
			i += 1
			fwdstep = 0
			backstep -= 1
	return map_sxe0, map_sxe1
"""