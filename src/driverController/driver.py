#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup

# Import custom modules
# Import package-wide constants


ClassDriver = webdriver.PhantomJS
ClassDriver = webdriver.Chrome

class webdriverTailored(ClassDriver):
	def __init__(self, path_driver):
		ClassDriver.__init__(self, path_driver)
		
		self.seq_iframe = []
		
	def detect_seq_iframe(self):
		self.seq_iframe = self.find_elements_by_tag_name('iframe')

	def get_pagesource_in_iframe(self, index):
		self.detect_seq_iframe()
		iframe = self.seq_iframe[index]
		self.switch_to_frame(iframe)
		psource = self.page_source
		
		soup = BeautifulSoup(psource, "html.parser")

		self.switch_to_default_content()
		return soup

	def kill(self):
		self.close()
		self.quit()


	def get_soup(self):
		psource = self.page_source
		soup = BeautifulSoup(psource, "html.parser")
		self.soup = soup
		return self.soup
"""
driver = webdriverTailored(PATH_DRIVER)
driver.get(url)
driver.detect_seq_iframe()
for i, iframe in enumerate(driver.seq_iframe):
	psrc = driver.get_pagesource_in_iframe(i)
	soup = BeautifulSoup(psrc, "html.parser")	
	for xpath in get_list_xpath(soup,[]): #, ["p", "script"]):
		print(xpath)
	print("#############################################################################")
driver.kill()
"""