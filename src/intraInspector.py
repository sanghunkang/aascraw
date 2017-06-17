#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import numpy as np

# Import custom modules
# Import package-wide constants
from constGlobal import *

class IntraInspector():
	def __init__(self, seq_xpath_encoded_2d, seq_xpath_encoded_occurence):
		self.seq_xpath_encoded_2d = seq_xpath_encoded_2d
		self.seq_xpath_encoded_occurence = seq_xpath_encoded_occurence

		self.seq_map_candidacy = []
		self.seq_set_canddt = []

		# Initial actions upon instantiation
		self.make_seq_map_candidacy()
		self.uniqfy_seq_map_candidacy()
		self.make_seq_set_canddt()

	def make_map_candidacy(self, i, xpath_encoded_occurence):
		var_input0 = self.calculate_index_var0(xpath_encoded_occurence)
		var_input1 = self.calculate_index_var1(xpath_encoded_occurence)
		map_candidacy = (i, var_input1, self.calculate_metric_candadacy(var_input0, var_input1))
		
		self.seq_map_candidacy.append(map_candidacy)

	def make_seq_map_candidacy(self):#, seq_xpath_encoded_occurence):
		seq_xpath_encoded_occurence = self.seq_xpath_encoded_occurence
		
		self.seq_map_candidacy = []
				
		for i, xpath_encoded_occurence in enumerate(seq_xpath_encoded_occurence):
			self.make_map_candidacy(i, xpath_encoded_occurence)

		self.seq_map_candidacy.sort(key=lambda x: x[2])
		self.seq_map_candidacy.reverse()	
		# self.seq_map_candidacy = seq_map_candidacy

	def uniqfy_seq_map_candidacy(self):
		seq_xpath_encoded_2d = self.seq_xpath_encoded_2d
		seq_map_candidacy = self.get_seq_map_candidacy()

		seq_xpath_encoded_2d_uniq = []
		seq_map_candidacy_uniq = []
		for map_candidacy in seq_map_candidacy:
			xpath_encoded_2d = seq_xpath_encoded_2d[map_candidacy[0]]
			xpath_encoded_2d_cut = xpath_encoded_2d[:map_candidacy[1]].tolist()
			
			if xpath_encoded_2d_cut not in seq_xpath_encoded_2d_uniq:
				seq_xpath_encoded_2d_uniq.append(xpath_encoded_2d_cut)
				seq_map_candidacy_uniq.append(map_candidacy)

		seq_map_candidacy_uniq.sort(key=lambda x: x[2])
		seq_map_candidacy_uniq.reverse()
		self.seq_map_candidacy_uniq = seq_map_candidacy_uniq

	def make_set_canddt(self, xpath_encoded_2d_target, map_candidacy):
		seq_xpath_encoded_2d = self.seq_xpath_encoded_2d

		set_canddt = []
		for i, xpath_encoded_2d_compared in enumerate(seq_xpath_encoded_2d):
			if xpath_encoded_2d_compared[:map_candidacy[1]].tolist() == xpath_encoded_2d_target[:map_candidacy[1]].tolist():
				set_canddt.append([i, xpath_encoded_2d_compared[map_candidacy[1]:]])

		return set_canddt

	def make_seq_set_canddt(self, cutoff=5):
		seq_xpath_encoded_2d = self.seq_xpath_encoded_2d
		seq_map_candidacy_uniq = self.get_seq_map_candidacy_uniq()

		seq_set_canddt = []
		for map_candidacy in seq_map_candidacy_uniq[:cutoff]: # Inspect top 5 candidate
			xpath_encoded_2d_target = seq_xpath_encoded_2d[map_candidacy[0]]
			seq_set_canddt.append(self.make_set_canddt(xpath_encoded_2d_target, map_candidacy))

		self.seq_set_canddt = seq_set_canddt

	def calculate_index_var0(self, xpath_encoded_occurence):
		# Maximum of numbers to tags
		var_input0 = max(xpath_encoded_occurence)
		return var_input0

	def calculate_index_var1(self, xpath_encoded_occurence):
		# Where the max appears
		var_input1 = xpath_encoded_occurence.tolist().index(max(xpath_encoded_occurence)) + 1
		return var_input1

	def calculate_metric_candadacy(self, var_input0, var_input1):
		# Some metric to select the most probable pattern(s)	
		var_output = (var_input0**2) - (var_input1**2)
		return var_output

	def get_seq_map_candidacy(self):
		return self.seq_map_candidacy

	def get_seq_map_candidacy_uniq(self):
		return self.seq_map_candidacy_uniq

	def get_seq_set_canddt(self):
		return self.seq_set_canddt


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