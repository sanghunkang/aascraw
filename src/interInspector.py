#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from functools import reduce

# Import external packages
import numpy as np

# Import custom modules
from driverController.locator import get_attr_elem, locate_element, get_eigentext

# Import package-wide constants
from constGlobal import *

class InterInspector():
	def __init__(self):
		self.seq_pageinfo = []

		self.intersect_xpath_encoded = []
	
		

	def receive_pageinfo(self, pageinfo):
		self.seq_pageinfo.append(pageinfo)
		
		# self.make_intersect_xpath_encoded()
		self.make_seq_seq_xpath()

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

	def make_seq_seq_xpath(self):
		seq_pageinfo = self.get_seq_pageinfo()
		seq_seq_xpath = [pageinfo.get_seq_xpath() for pageinfo in seq_pageinfo]
		self.seq_seq_xpath = seq_seq_xpath

	def make_seq_xpath_target(self):
		seq_seq_xpath = self.get_seq_seq_xpath()

		seq_len = [len(seq_xpath) for seq_xpath in seq_seq_xpath]
		index = seq_len.index(min(seq_len))

		seq_xpath_target = seq_seq_xpath[index]
		self.seq_xpath_target = seq_xpath_target

	def make_intersect_xpath(self):
		# Doesn't seem perfect
		seq_xpath_target = self.get_seq_xpath_target()
		seq_seq_xpath = self.get_seq_seq_xpath()

		intersect_xpath = []
		for i, xpath in enumerate(seq_xpath_target):
			is_repeating = True
			for seq_xpath in seq_seq_xpath:
				if xpath not in seq_xpath:
					is_repeating == False
					break
			if is_repeating == True:
				# print(xpath)
				intersect_xpath.append(xpath)
		
		self.intersect_xpath = intersect_xpath

	def make_seq_xpath_canddt_inter(self):
		self.make_seq_xpath_target()
		self.make_intersect_xpath()

		seq_pageinfo = self.get_seq_pageinfo()
		intersect_xpath = self.get_intersect_xpath()

		seq_xpath_canddt_inter = []
		for i, xpath in enumerate(intersect_xpath):
			try:
				seq_elem_located = [locate_element(pageinfo.get_soup(), xpath, get_attr_elem)[-1] for pageinfo in seq_pageinfo]
				seq_eigentext = [get_eigentext(elem_located) for elem_located in seq_elem_located]
				
				eigentext0 = seq_eigentext[0]
				eigentext1 = seq_eigentext[1]
				eigentext2 = seq_eigentext[2]

				print(i, "#############################################################################")
				print(xpath)
				if eigentext0 != eigentext1 or eigentext1 != eigentext2:
					print(eigentext0)
					print("_______________________________________________________________")
					print(eigentext1)
					print("_______________________________________________________________")
					print(eigentext2)
					print("_______________________________________________________________")
					seq_xpath_canddt_inter.append(xpath)

			except IndexError:
				print(IndexError)
			except TypeError:
				print(TypeError)
			i += 1
		self.seq_xpath_canddt_inter = seq_xpath_canddt_inter
		# return seq_xpath_canddt_inter

	# Getters ... well defined
	def get_seq_pageinfo(self):
		return self.seq_pageinfo

	def get_shape_intersect(self):
		return self.shape_intersect

	def get_intersect_xpath_encoded(self):
		# self.make_intersect_xpath_encoded()
		return self.intersect_xpath_encoded

	def get_seq_seq_xpath(self):
		return self.seq_seq_xpath

	def get_seq_xpath_target(self):
		return self.seq_xpath_target

	def get_intersect_xpath(self):
		return self.intersect_xpath

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

# def get_seq_xpath_target(seq_seq_xpath):
# 	seq_len = [len(seq_xpath) for seq_xpath in seq_seq_xpath]
# 	index = seq_len.index(min(seq_len))

# 	seq_xpath_target = seq_seq_xpath[index]
# 	return seq_xpath_target, index

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
"""
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



# def get_filteredseq_xpath(seq_xpath, seq_map_xpath):
# 	filteredseq_xpath = []
# 	for map_xpath in seq_map_xpath:
# 		filteredseq_xpath.append(seq_xpath[map_xpath])
# 	return filteredseq_xpath