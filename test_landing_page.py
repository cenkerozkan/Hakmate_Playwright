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
    page.goto(BASE_URL)

    expect(page).to_have_title("HakMate")

def test_landing_page_login_button(page: Page):
    page.goto(BASE_URL)

    page.get_by_role(role="button", name="Giriş Yap").click()
    expect(page.get_by_role(role="textbox", name="E-posta")).to_be_visible()

    # Fetch all the buttons in the page.
    buttons:Locator = page.get_by_role(role="button", name="Giriş Yap")
    buttons.nth(1).click() # Click the second one which is what we are looking for.

    expect(page.get_by_text(text="Lütfen geçerli bir e-posta adresi giriniz")).to_be_visible()
    expect(page.get_by_text(text="Şifre en az 6 karakter uzunluğunda olmalıdır")).to_be_visible()

def test_login_with_user(page: Page):
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
    page.goto(BASE_URL)

    # Go to chat page without an account.
    page.get_by_role(role="button", name="Chat").click()

    expect(page.get_by_role(role="textbox"))

    text_boxes:Locator = page.get_by_role(role="textbox")
    text_boxes.nth(0).fill("Playwright Test!")

    buttons:Locator = page.get_by_role(role="button")
    buttons.nth(2).click() # Button 2 is for creating chat.
    time.sleep(5)