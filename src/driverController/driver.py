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

	def send_info_signin(self, user_id, user_pw):
		# Shabby yet...
		seq_canddt_input = self.find_elements_by_tag_name("input")
		for canddt_input in seq_canddt_input:
			type_input = canddt_input.get_attribute("type")
			if "text" in type_input:
				canddt_input.send_keys(user_id)
				is_inserted_userid = True

			if "password" in type_input:
				canddt_input.send_keys(user_pw)
				is_inserted_userpw = True

			if "submit" in type_input and is_inserted_userid and is_inserted_userpw:
				canddt_input.click()
				break

	def kill(self):
		self.close()
		self.quit()

	# Getters
	def get_soup_from_iframe(self, index):
		iframe = self.find_elements_by_tag_name('iframe')[index]
		self.switch_to_frame(iframe)
		
		psource = self.page_source		
		soup = BeautifulSoup(psource, "html.parser")

		self.switch_to_default_content()
		return soup

	def get_soup(self):
		psource = self.page_source
		soup = BeautifulSoup(psource, "html.parser")
		return soup