#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

class intraInspector():
	def __init__(self, seq_xpath_encoded_3d):
		pass

def get_max_size_window(seq_xpath_encoded_3d):
	max_size_window = seq_xpath_encoded_3d.shape[0]//2
	return max_size_window

def calculate_max_index_start(seq_xpath_encoded_3d, size_window):
	max_index_start = seq_xpath_encoded_3d.shape[0] - size_window
	return max_index_start

def make_tsr_slice(seq_xpath_encoded_3d, index_start, size_window):
	subseq_xpath_encoded_3d = seq_xpath_encoded_3d[index_start: index_start + size_window]
	return subseq_xpath_encoded_3d

def get_seq_index_canddt(seq_xpath_encoded_3d, depth_eval):
	seq_index_canddt = []
	for i, xpath_encoded_3d in enumerate(seq_xpath_encoded_3d):	
		if np.sum(xpath_encoded_3d[-depth_eval]) > 0 and np.sum(xpath_encoded_3d[-depth_eval+1:]) == 0:
			seq_index_canddt.append(i)
	return np.array(seq_index_canddt, dtype=np.int32)

#############################################################################
def encode_xpath_2d(xpath_encoded):
	xpath_encoded_2d = np.zeros(shape=(len(xpath_encoded), len(SEQ_TAGCODE)), dtype=np.int32)
	for i, elem in enumerate(xpath_encoded):
		xpath_encoded_2d[i, elem] = 1 # int(elem)
	return xpath_encoded_2d

# def make_tsr_slice(seq_xpath_encoded, index, size_slice):
# 	subseq_xpath_encoded = seq_xpath_encoded[index: index + size_slice]
# 	range_xpath = subseq_xpath_encoded.shape[1]
	
# 	tsr_slice = np.zeros(shape=(size_slice, range_xpath, len(SEQ_TAGCODE)), dtype=np.int32)
# 	for n, xpath_encoded in enumerate(subseq_xpath_encoded):
# 		tsr_slice[n] = encode_xpath_2d(xpath_encoded)
# 	return tsr_slice

# def get_seq_index_canddt(seq_xpath_encoded, depth_eval):
# 	seq_index_canddt = []
# 	for i, xpath_encoded in enumerate(seq_xpath_encoded):	
# 		if xpath_encoded[depth_eval] > 0 and np.sum(xpath_encoded[depth_eval+1:]) == 0:
# 			seq_index_canddt.append(i)
# 	return np.array(seq_index_canddt, dtype=np.int32)

def calculate_dist_tsr(tsr0, tsr1):
	dist = np.sum((tsr0 - tsr1)**2)
	return dist

def update_seq_index_canddt(seq_xpath_encoded, seq_index_canddt, size_slice):
	seq_index_canddt_new = []
	for i, index_canddt0 in enumerate(seq_index_canddt):
		tsr0 = make_tsr_slice(seq_xpath_encoded, index_canddt0, size_slice)

		for j, index_canddt1 in enumerate(seq_index_canddt[i+1:]):
			tsr1 = make_tsr_slice(seq_xpath_encoded, index_canddt1, size_slice)
			dist = calculate_dist_tsr(tsr0, tsr1)
			# print(index_canddt0, index_canddt1, dist)		

			if dist < 1 and index_canddt0 not in seq_index_canddt_new:
				seq_index_canddt_new.append(index_canddt0)

	seq_index_canddt_new = np.array(seq_index_canddt_new, dtype=np.int32)
	return seq_index_canddt_new