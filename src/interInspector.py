#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from functools import reduce

# Import external packages
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

class InterInspector():
	def __init__(self):
		self.seq_pageinfo = []

		self.intersect_xpath_encoded = []
	
		

	def receive_pageinfo(self, pageinfo):
		self.seq_pageinfo.append(pageinfo)
		self.make_intersect_xpath_encoded()

	def calculate_shape_intersect(self):
		seq_pageinfo = self.get_seq_pageinfo()

		nrows = min([pageinfo.get_uniqseq_xpath_encoded().shape[0] for pageinfo in seq_pageinfo])
		ncols = min([pageinfo.get_uniqseq_xpath_encoded().shape[1] for pageinfo in seq_pageinfo])

		self.shape_intersect = (nrows, ncols)

	def _make_seq_for_intersect(self):
		seq_pageinfo = self.get_seq_pageinfo()
		nrows, ncols = self.get_shape_intersect()

		dtype = {
			'names':['f{}'.format(i) for i in range(ncols)], 
			'formats':ncols * [np.int32]
		}
		seq_for_intersect = []
		for pageinfo in seq_pageinfo:
			for_intersect = pageinfo.get_uniqseq_xpath_encoded().view(dtype)
			seq_for_intersect.append(for_intersect)

		return seq_for_intersect

	def make_intersect_xpath_encoded(self):
		self.calculate_shape_intersect()

		nrows, ncols = self.get_shape_intersect()
		seq_for_intersect = self._make_seq_for_intersect()

		intersect_xpath_encoded = reduce(np.intersect1d, seq_for_intersect)
		intersect_xpath_encoded = intersect_xpath_encoded.view(np.int32).reshape(-1, ncols)
		
		self.intersect_xpath_encoded = intersect_xpath_encoded

	def get_seq_pageinfo(self):
		return self.seq_pageinfo

	def get_shape_intersect(self):
		return self.shape_intersect

	def get_intersect_xpath_encoded(self):
		# self.make_intersect_xpath_encoded()
		return self.intersect_xpath_encoded


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
def shrink1st_seq_xpath_encoded(seq_xpath_encoded, seq_map_xpath):
	shrunkseq_xpath_encoded = np.zeros(shape=(seq_map_xpath.shape[0], seq_xpath_encoded.shape[1]), dtype=np.int32)
	for map_xpath in seq_map_xpath:
		shrunkseq_xpath_encoded[map_xpath[1]] = seq_xpath_encoded[map_xpath[0]]
	return shrunkseq_xpath_encoded

def get_seq_xpath_encoded_target(seq_seq_xpath_encoded):
	seq_len = [len(seq_xpath_encoded) for seq_xpath_encoded in seq_seq_xpath_encoded]
	index = seq_len.index(min(seq_len))

	seq_xpath_encoded_target = seq_seq_xpath_encoded[index]
	return seq_xpath_encoded_target, index

def simpleshrink(seq_xpath_target, seq_seq_xpath_encoded):
	seq_xpath_simpleshrink = []
	for i, xpath_encoded in enumerate(seq_xpath_encoded_target):
		is_repeating = True
		for seq_xpath_encoded in seq_seq_xpath_encoded:
			if xpath_encoded not in seq_xpath_encoded:
				is_repeating == False
				break
		if is_repeating == True:
			print(xpath_encoded)
			seq_xpath_simpleshrink.append(i)
	return seq_xpath_simpleshrink

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



def get_filteredseq_xpath(seq_xpath, seq_map_xpath):
	filteredseq_xpath = []
	for map_xpath in seq_map_xpath:
		filteredseq_xpath.append(seq_xpath[map_xpath])
	return filteredseq_xpath