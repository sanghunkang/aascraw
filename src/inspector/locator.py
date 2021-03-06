#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
import re

# Import external packages
# Import custom modules
# Import package-wide constants

def get_children_direct(elem, tag_of_interest=None): # afraid of breaking this :()
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
	try:
		type_tag_parent, index_tag_parent, xpath_descendent = xpath.split("/", 2)
		elem_new = get_children_direct(elem, type_tag_parent)[int(index_tag_parent)]
		
		# print(elem_new.attrs)
		ret.append(func_to_rpt(elem_new))
		if len(xpath_descendent.split("/")) > 1:		
			return locate_element(elem_new, xpath_descendent, func_to_rpt, ret)
		else:
			return ret
	except ValueError:
		return None

def get_eigentext(elem):
	try:
		elem_str = str(elem)
		pattern = re.compile(r"<.*?>(.*?)<.*?>", re.DOTALL)
		str_match = pattern.match(elem_str).group(0)	
		str_stripped = re.sub(r"<.*?>", "", str_match, re.DOTALL)
	except AttributeError:
		str_stripped = "FAILED"
	return str_stripped

def get_eigentext_bw(elem):
	try:
		elem_str = str(elem)
		pattern = re.compile(r"<.*?>(.*?)<.*?>$", re.DOTALL)
		str_match = pattern.match(elem_str).group(0)	
		str_stripped = re.sub(r"<.*?>", "", str_match, re.DOTALL)
	except AttributeError:
		str_stripped = "FAILED"
	return str_stripped

class Locator():
	def __init__(self, pageinfo):
		self.pageinfo = pageinfo

	def generate_soup_inner(self, soup, name_tag, index_tag):
		# try:
		children_1st = soup.findChildren()[0]
		children_direct = [children_1st] + children_1st.find_next_siblings()
		children_direct = [child for child in children_direct if child.name==name_tag]	
		# except IndexError:
		# 	children_direct = []

		soup_inner = children_direct[index_tag]
		return soup_inner

	def locate_element(self, soup, queue_xpath):
		name_tag = queue_xpath.pop(0)
		index_tag = int(queue_xpath.pop(0))
		
		soup_inner = self.generate_soup_inner(soup, name_tag, index_tag)

		if len(queue_xpath) != 0: return self.locate_element(soup_inner, queue_xpath)
		elif len(queue_xpath) == 0: return soup_inner

	def generate_eigentext(self, xpath):	
		pageinfo = self.get_pageinfo()
		soup_uppermost = pageinfo.get_soup()
		queue_xpath = xpath.split("/")[:-1]

		elem = self.locate_element(soup_uppermost, queue_xpath)
		
		try:
			elem_str = str(elem)
			pattern = re.compile(r"<.*?>(.*?)<.*?>", re.DOTALL)
			str_match = pattern.match(elem_str).group(0)	
			str_stripped = re.sub(r"<.*?>", "", str_match, re.DOTALL)
		except AttributeError:
			str_stripped = "FAILED"
		return str_stripped

	def get_pageinfo(self):
		return self.pageinfo