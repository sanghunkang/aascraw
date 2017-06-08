#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import re

# Import external packages
# Import custom modules
# Import package-wide constants

def get_children_direct(elem, tag_of_interest=None):
	try:
		children_1st = elem.findChildren()[0]
		children_direct = [children_1st] + children_1st.find_next_siblings()
	except IndexError:
		children_direct = []

	if tag_of_interest == None:
		children_direct_relevant = children_direct
	else:
		children_direct_relevant = []
		for child_direct in children_direct:
			if re.search(r"^<" + re.escape(tag_of_interest) + r".+", str(child_direct)):
				children_direct_relevant.append(child_direct)

	return children_direct_relevant

def get_attr_elem(elem):
	# return elem.attrs
	return elem

def locate_element(elem, xpath, func_to_rpt, ret=[]):
	type_tag_parent, index_tag_parent, xpath_descendent = xpath.split("/", 2)
	elem_new = get_children_direct(elem, type_tag_parent)[int(index_tag_parent)]
	
	# print(elem_new.attrs)
	ret.append(func_to_rpt(elem_new))
	if len(xpath_descendent.split("/")) > 1:		
		return locate_element(elem_new, xpath_descendent, func_to_rpt, ret)
	else:
		return ret