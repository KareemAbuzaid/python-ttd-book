from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from .base import FunctionalTest
User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # just visit the domain to get a cookie
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path='/'))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # logged in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        # this is a logged in users
        self.create_pre_authenticated_session('edith@example.com')

        # user goes to homepage and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('List item 1')
        self.add_list_item('List item 2')
        first_list_url = self.browser.current_url

        # user can see the "My lists" link for the
        # first time
        self.browser.find_element_by_link_text('My lists').click()

        # user can see that his/her list is there and correctly
        # labeled
        self.wait_for(lambda: self.browser.find_element_by_link_text('List item 1'))
        self.browser.find_element_by_link_text('List item 2').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_link_url))

        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # user starts another list just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # new list should appear under 'my lists'
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # once user logs out, the 'my lists' option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text('My lists'), []))

