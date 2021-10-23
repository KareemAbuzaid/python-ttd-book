import os
import time
from unittest import skip
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        
        self.browser.get(self.live_server_url)
        
        # add an empty item
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # add a non empty item
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.wait_for_row_in_list_table('1: Buy milk')

        # add an empty item again
        self.get_item_input_box().send_keys(Keys.ENTER)

        # see an error message
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        
        # can add items after error
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

