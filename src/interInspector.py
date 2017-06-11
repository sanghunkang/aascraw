#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

def get_unqseq_xpath_encoded(seq_xpath_encoded):
	unqseq_xpath_encoded = np.vstack({tuple(row) for row in seq_xpath_encoded})
	return unqseq_xpath_encoded

def get_intersect_xpath_encoded(unqseq_xpath_encoded_0, unqseq_xpath_encoded_1):
	nrows, ncols = unqseq_xpath_encoded_0.shape
	dtype={
		'names':['f{}'.format(i) for i in range(ncols)], 
		'formats':ncols * [unqseq_xpath_encoded_0.dtype]
	}

	intersect_xpath_encoded = np.intersect1d(unqseq_xpath_encoded_0.view(dtype), unqseq_xpath_encoded_1.view(dtype))
	intersect_xpath_encoded = intersect_xpath_encoded.view(unqseq_xpath_encoded_1.dtype).reshape(-1, ncols)
	return intersect_xpath_encoded

def make_map(seq_xpath_encoded, intersect_xpath_encoded):
	seq_map_xpath = np.zeros(shape=(seq_xpath_encoded.shape[0],2), dtype=np.int32)
	seq_map_xpath.fill(-1)
	
	index_mapped = 0
	for i, xpath_encoded in enumerate(seq_xpath_encoded):
		for j, xpath_encoded_unq in enumerate(intersect_xpath_encoded):
			if np.array_equal(xpath_encoded, xpath_encoded_unq):
				seq_map_xpath[i] = np.array([i, index_mapped], dtype=np.int32)
				index_mapped += 1
	seq_map_xpath = seq_map_xpath[~np.all(seq_map_xpath == -1, axis=1)]
	return seq_map_xpath

# possilbly skip this stage
def shrink1st_seq_xpath_encoded(seq_xpath_encoded, seq_map_xpath):
	shrunkseq_xpath_encoded = np.zeros(shape=(seq_map_xpath.shape[0], seq_xpath_encoded.shape[1]), dtype=np.int32)
	for map_xpath in seq_map_xpath:
		shrunkseq_xpath_encoded[map_xpath[1]] = seq_xpath_encoded[map_xpath[0]]
	return shrunkseq_xpath_encoded

def shrink2nd_seq_xpath_encoded(seq_xpath_encoded_0, seq_xpath_encoded_1):
	if len(seq_xpath_encoded_0) < len(seq_xpath_encoded_1):
		sxe0, sxe1 = seq_xpath_encoded_0, seq_xpath_encoded_1
	else:
		sxe0, sxe1 = seq_xpath_encoded_1, seq_xpath_encoded_0

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

def get_filteredseq_xpath(seq_xpath, seq_map_xpath):#, range_xpath):
	# filteredseq_xpath = np.zeros(shape=(len(seq_map_xpath), range_xpath))
	# for i, map_xpath in enumerate(seq_map_xpath):
	# 	filteredseq_xpath[i] = seq_xpath[map_xpath]
	filteredseq_xpath = []
	for map_xpath in seq_map_xpath:
		filteredseq_xpath.append(seq_xpath[map_xpath])
	return filteredseq_xpath