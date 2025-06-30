"""
This file is for testing the landing page of hakmate vercel application.
"""

import time
import re
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect, Locator

# Note for myself: URLs always should start with http or https.
BASE_URL: str = "https://hakmate-frontend.vercel.app"
load_dotenv()

def test_landing_page_title(page: Page):
    """
    Goes to the landing page of hakmate vercel application.
    Checks if the title is correct.
    """
    page.goto(BASE_URL)

    expect(page).to_have_title("HakMate")

def test_landing_page_login_button(page: Page):
    """
    Clicks the login button on the landing page.
    Checks if the login screen correct or not.
    """
    page.goto(BASE_URL)

    page.get_by_role(role="button", name="Giriş Yap").click()
    expect(page.get_by_role(role="textbox", name="E-posta")).to_be_visible()

    # Fetch all the buttons in the page.
    buttons:Locator = page.get_by_role(role="button", name="Giriş Yap")
    buttons.nth(1).click() # Click the second one which is what we are looking for.

    expect(page.get_by_text(text="Lütfen geçerli bir e-posta adresi giriniz")).to_be_visible()
    expect(page.get_by_text(text="Şifre en az 6 karakter uzunluğunda olmalıdır")).to_be_visible()

def test_login_with_user(page: Page):
    """
    Goes to login screen, fills the email and password
    then logs in to the application.
    """
    page.goto(BASE_URL)

    # Go to login page.
    page.get_by_role(role="button", name="Giriş Yap").click()

    # Locate the email and password text boxes.
    text_boxes:Locator = page.get_by_role(role="textbox")
    text_boxes.nth(0).fill(os.getenv("HAKMATE_EMAIL"))
    text_boxes.nth(1).fill(os.getenv("HAKMATE_PASSWORD"))

    # Login
    buttons:Locator = page.get_by_role(role="button", name="Giriş Yap")
    buttons.nth(0).click()

def test_chat_screen_with_anon(page: Page):
    """
    Goes to chat screen without an account, and
    creates a new chat
    """
    page.goto(BASE_URL)

    # Go to chat page without an account.
    page.get_by_role(role="button", name="Chat").click()

    expect(page.get_by_role(role="textbox"))

    text_boxes:Locator = page.get_by_role(role="textbox")
    text_boxes.nth(0).fill("Playwright Test!")

    buttons:Locator = page.get_by_role(role="button")
    buttons.nth(2).click() # Button 2 is for creating chat.

    # Check if the chat is created or not.
    expect(page.get_by_text(text="Playwright Test!")).to_be_visible()


def test_chat_screen_anon_response(page: Page):
    """
    This one goes to anonymous chat, creates a new chat.
    Sends a test message to the system.
    """
    page.goto(BASE_URL)

    page.get_by_role(role="button", name="Chat").click()

    # Anonymous indicator.
    expect(page.get_by_text(text="Anonymous session")).to_be_visible()

    # Retrieve text_boxes and buttons
    text_boxes: Locator = page.get_by_role(role="textbox")
    buttons: Locator = page.get_by_role(role="button")

    # Let's create the chat.
    text_boxes.nth(0).fill("Playwright Test!")
    buttons.nth(2).click()

    expect(page.get_by_text(text="Playwright Test!")).to_be_visible()

    # Now click the chat button again
    chat: Locator = page.get_by_text(text="Playwright Test!")
    chat.click()

    # Now this will trigger an extra button to render.
    text_boxes.nth(1).fill("This is a playwright test message")

    buttons = page.get_by_role(role="button")
    buttons.nth(5).click() # 5th button is for sending a message.

    # Wait for 5 seconds
    time.sleep(5)

    # Now we are expecting response with this class id.
    expect(page.locator("css=[class^MuiBox]"))