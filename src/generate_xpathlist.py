#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
from urllib import request

# Import 3rd-party packages
# import requests # do I need this?

from bs4 import BeautifulSoup
# from selenium import webdriver

def get_HTMLdoc(url):
	req = request.urlopen(url)
	charset = req.info().get_content_charset()
	ret = req.read().decode(charset)
	return ret

def get_list_xpath(doc, path_prev="", ret=[]):
	list_tmp = []
	for child in doc.children:
		i = list_tmp.count(child.name)
		list_tmp.append(child.name)

		if hasattr(child, "children") == True and len(list(child.children)) <= 1:			
			ret.append(path_prev.lstrip("/") + "/"+ child.name + ":{0}".format(i) + "/PATHEND")
		elif hasattr(child, "children") == True:
			get_list_xpath(child, path_prev + "/"+ child.name + ":{0}".format(i), ret)
	
	return ret