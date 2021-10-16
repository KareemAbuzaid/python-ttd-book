import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        
        # Edith hears about this great new to-do
        # app, she checks out the homepage
        self.browser.get('http://localhost:8000')
        
        # she notices the page title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # she is invited to add a todo item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # she types a to do
        inputbox.send_keys('Buy peacock feathers')

        # when she hits enter the page updates
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # types in another to do
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('But peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows  = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])
        
        self.fail('Finish the tests!')

if __name__ == '__main__':
    unittest.main()

