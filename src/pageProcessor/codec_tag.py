#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import numpy as np

# Import custom modules
# Import package-wide constants
from const_global import *

def encode_xpath(xpath, seq_tagcode, range_xpath):
	xpath_encoded = np.zeros(shape=(2, range_xpath), dtype=np.int32)
	seq_elem = xpath.split("/")
	
	for i in range(0, len(seq_elem)-1, 2):
		try:
			index = int(i/2)
			xpath_encoded[0, index] = SEQ_TAGCODE.index(seq_elem[i])
			xpath_encoded[1, index] = int(seq_elem[i+1])
		except ValueError: # Trivial error not so important for now
			pass

	return xpath_encoded

def encode_xpath_2d(xpath_encoded):
	xpath_encoded_2d = np.zeros(shape=(len(xpath_encoded), len(SEQ_TAGCODE)), dtype=np.int32)
	for i, elem in enumerate(xpath_encoded):
		# xpath_encoded_2d[i, int(elem)] = 1
		xpath_encoded_2d[i, elem] = 1	
	return xpath_encoded_2d

def make_seq_xpath_encoded(seq_xpath, shape):
	seq_xpath_encoded = np.zeros(shape=shape, dtype=np.int32)
	for i, xpath in enumerate(seq_xpath):
		seq_xpath_encoded[i] = encode_xpath(xpath, SEQ_TAGCODE, shape[1])[0]
	return seq_xpath_encoded

def make_tsr_slice(seq_xpath_encoded, index, size_slice):
	subseq_xpath_encoded = seq_xpath_encoded[index: index + size_slice]
	range_xpath = subseq_xpath_encoded.shape[1]
	
	tsr_slice = np.zeros(shape=(size_slice, range_xpath, len(SEQ_TAGCODE)), dtype=np.int32)
	for n, xpath_encoded in enumerate(subseq_xpath_encoded):
		tsr_slice[n] = encode_xpath_2d(xpath_encoded)
	return tsr_slice

def get_seq_index_canddt(seq_xpath_encoded, depth_eval):
	# seq_index_canddt = [i for i, xpath_encoded in enumerate(seq_xpath_encoded) if np.min(xpath_encoded[depth_eval:]) > 0]
	# return seq_index_canddt
	seq_index_canddt = []
	for i, xpath_encoded in enumerate(seq_xpath_encoded):	
		if xpath_encoded[depth_eval] > 0 and np.sum(xpath_encoded[depth_eval+1:]) == 0:
			seq_index_canddt.append(i)
	return np.array(seq_index_canddt, dtype=np.int32)

def update_seq_index_canddt(seq_xpath_encoded, seq_index_canddt, size_slice):
	seq_index_canddt_new = []
	for i, index_canddt0 in enumerate(seq_index_canddt):
		tsr0 = make_tsr_slice(seq_xpath_encoded, index_canddt0, size_slice)

		for j, index_canddt1 in enumerate(seq_index_canddt[i+1:]):
			tsr1 = make_tsr_slice(seq_xpath_encoded, index_canddt1, size_slice)

			diff = tsr0 - tsr1
			dist = np.sum(diff**2)
			print(index_canddt0, index_canddt1, dist)			

			if dist < 2 and index_canddt0 not in seq_index_canddt_new:
				seq_index_canddt_new.append(index_canddt0)

	seq_index_canddt_new = np.array(seq_index_canddt_new, dtype=np.int32)
	print(size_slice)
	print("#############################################################################")
	return seq_index_canddt_new