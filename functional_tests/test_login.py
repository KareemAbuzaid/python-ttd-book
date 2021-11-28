from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'kareem.abuzaid123@gmail.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):

        # enter email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # message stating that email has been sent
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element_by_tag_name('body').text))

        # see email message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # the url link is in the mail
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # click link
        self.browser.get(url)

        # user is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # user logs out
        self.browser.find_element_by_link_text('Log out').click()

        # logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)

