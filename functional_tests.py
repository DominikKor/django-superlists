import os
import time
import unittest

import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists_dj.settings")
django.setup()

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        opts =  FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=opts)
        staging_server = os.environ.get("STAGING_SERVER")
        print("Staging server:", staging_server)
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_list_in_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(
            row_text, [row.text for row in rows],
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_list_in_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_list_in_table("1: Buy peacock feathers")
        self.check_for_row_list_in_table("2: Use peacock feathers to make a fly")

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings="ignore")
