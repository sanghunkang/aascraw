#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from urllib import request

# Import external packages
import numpy as np

def define_dim(seq_xpath):
	seq_tag_on = []
	for xpath in seq_xpath:
		seq_tag_on += [tag for i, tag in enumerate(xpath.split("/")[:-1]) if i % 2 == 0]
	return list(set(seq_tag_on))
	# printseq_tag_on)

def get_depth_max(seq_xpath):
	seq_depth = [(len(xpath.split("/"))-1)//2 for xpath in seq_xpath]
	depth_max = max(seq_depth)
	return depth_max

# def func_serialize_elem_data(xpath, elems_located):
# 	xpath # some action
# 	elems_located[-1] # some action
# 	return [] # some list ... or list of list

def subsample_seq_xpath(seq_xpath, size_subsample):
	len_seq_xpath = len(seq_xpath)
	num_subsample = len_seq_xpath // size_subsample
	seq_subsample = []
	for i in range(num_subsample):
		subsample = seq_xpath[i*size_subsample: (i+1)*size_subsample]
		seq_subsample.append(subsample)
	return seq_subsample

def matrixify_xpath(xpath, depth, vec_index):
	len_vec_index = len(vec_index)
	seq_tag = [tag for i, tag in enumerate(xpath.split("/")[:-1]) if i % 2 == 0]

	mat_xpath = np.zeros(shape=(depth, len_vec_index))
	for i, tag in enumerate(seq_tag):
		mat_xpath[i, vec_index.index(tag)] = 1
	return mat_xpath

def tensify_sumsample(subsample, depth, vec_index):
	size_sumsample = len(subsample)
	len_vec_index = len(vec_index)
	tsr = np.zeros(shape=(size_sumsample, depth, len_vec_index))
	
	for i, xpath in enumerate(subsample):
		tsr[i] = matrixify_xpath(xpath, depth, vec_index)
	
	return tsr


def calculate_similarity(tsr_0, tsr_1):
	tsr_dist = tsr_0 - tsr_1
	dist = np.sum(tsr_dist)
	return dist