#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import re

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

def locate_element(elem, xpath, ret=[]):
	tag_parent = xpath.split("/", 1)[0]
	xpath_descendent = xpath.split("/", 1)[1]

	type_tag_parent = tag_parent.split(":")[0]
	index_tag_parent = int(tag_parent.split(":")[1])

	# print(type_tag_parent + "   " + str(index_tag_parent))
	# print(xpath_descendent)
		
	elem_new = get_children_direct(elem, type_tag_parent)[index_tag_parent]
	
	if len(xpath_descendent.split("/")) > 1:
		return locate_element(elem_new, xpath_descendent)
	else:
		return elem_new