"""
    playwright install command downloads the headless browsers
    into the /Users/user/Libray/Caches/ms-playwright directory.
    Do not forget to remove those when you're done.
"""

import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    """
    This methods goes to playwright.dev and
    expects a title that contains "Fast and re"
    substring.
    """
    page.goto("https://playwright.dev/")

    expect(page).to_have_title(re.compile("Fast and re"))

def test_get_started_link(page: Page):
    """
    This method goes to playwright.dev and finds a link
    that says "Get Started". Then clicks it, and starts
    to expect a page header page element that says Installation.
    """
    page.goto("https://playwright.dev/")

    page.get_by_role(role="link", name="Get started").click()

    expect(page.get_by_role(role="heading", name="Installation")).to_be_visible()