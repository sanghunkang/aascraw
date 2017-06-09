#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import built-in packages
# Import external packages
import selenium
from selenium import webdriver

# Import custom modules
# Import package-wide constants


ClassDriver = webdriver.PhantomJS

class webdriverTailored(ClassDriver):
	def __init__(self, path_driver):
		ClassDriver.__init__(self, path_driver)
		
		self.seq_iframe = []
		
	def detect_seq_iframe(self):
		self.seq_iframe = self.find_elements_by_tag_name('iframe')

	def get_pagesource_in_iframe(self, index):
		iframe = self.seq_iframe[index]
		self.switch_to_frame(iframe)
		ret = self.page_source
		
		self.switch_to_default_content()
		return ret

	def kill(self):
		self.close()
		self.quit()