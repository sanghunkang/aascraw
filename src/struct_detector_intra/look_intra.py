#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from urllib import request

# Import external packages
import numpy as np

# def get_seq_subseq(seq_xpath, len_subseq, padding):
# 	seq_subseq = []
# 	for i in range(len(seq_xpath)//len_subseq):
# 		subseq = seq_xpath[i*len_subseq + padding: (i+1)*len_subseq + padding]
# 		seq_subseq.append(subseq)	
# 	return seq_subseq

def get_seq_subseq(seq_xpath, len_subseq):
	seq_subseq = []
	for i in range(len(seq_xpath) - len_subseq):
		subseq = seq_xpath[i:i + len_subseq]
		seq_subseq.append(subseq)	
	return seq_subseq

def get_seq_tag_uniq(seq_xpath):
	"""
	(yet to be described)
	"""
	seq_tag = []
	for xpath in seq_xpath:
		seq_tag += [tag for i, tag in enumerate(xpath.split("/")[:-1]) if i % 2 == 0]
	seq_tag_uniq = list(set(seq_tag))
	return seq_tag_uniq

def get_range_tag(seq_tag_uniq):
	"""
	Get number of different tags apperearing on the entire document 
	"""
	return len(seq_tag_uniq)

def get_range_xpath(seq_xpath):
	"""
	Get the (rendered) maximum depth of xpaths
	"""
	seq_depth = [len(xpath.split("/")) for xpath in seq_xpath]
	depth_max = max(seq_depth)//2
	return depth_max

def make_matrix_xpath(xpath, seq_tag_uniq, shape):
	"""
	shape = (range_xpath, range_tag)
	"""
	seq_tag = [tag for i, tag in enumerate(xpath.split("/")[:-1]) if i % 2 == 0]
	
	matrix_xpath = np.zeros(shape=shape)
	for i, tag in enumerate(seq_tag):
		matrix_xpath[i, seq_tag_uniq.index(tag)] = 1
	
	return matrix_xpath

def make_tsr_subseq(subseq, seq_tag_uniq, shape):
	"""
	shape = (len_subseq, range_xpath, range_tag)
	"""
	tsr_subseq = np.zeros(shape=shape)	
	for i, xpath in enumerate(subseq):
		tsr_subseq[i] = make_matrix_xpath(xpath, seq_tag_uniq, (shape[1], shape[2]))
	
	return tsr_subseq

def calculate_dist_tsr(tsr0, tsr1):
	dist = abs(np.sum(tsr0 - tsr1))
	return dist

def make_seq_pairdistmap(seq_subseq, seq_tag_uniq, shape):
	"""
	returns sequence of pair-distance map
	"""
	seq_pairdistmap = []
	for i, subseq0 in enumerate(seq_subseq):
		tsr0 = make_tsr_subseq(subseq0, seq_tag_uniq, shape)
		for j, subseq1 in enumerate(seq_subseq[i+1:]):
			tsr1 = make_tsr_subseq(subseq1, seq_tag_uniq, shape)

			pairdistmap = ((i, i+1 + j), calculate_dist_tsr(tsr0, tsr1))
			seq_pairdistmap.append(pairdistmap)
	return seq_pairdistmap

def make_seq_weightmap():
	pass