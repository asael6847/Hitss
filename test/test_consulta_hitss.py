from playwright.sync_api import sync_playwright, expect, Page, TimeoutError as PlaywrightTimeoutError
from src.abilities.browse_the_web import BrowseTheWeb
from src.actors.actor import Actor
from src.tasks.open_home_page import OpenHomePage
from src.tasks.navigate_to_practicas_tecnologicas import NavigateToPracticasTecnologicas
import time

def test_consulta_hitss():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless = False)

        context = browser.new_context()
        page = context.new_page()

        asael = Actor("Asael")
        web_ability = BrowseTheWeb.with_(page)
        asael.can(web_ability)

        asael.attempts_to(OpenHomePage("https://www.hitss.com"))


        asael.attempts_to(NavigateToPracticasTecnologicas())



        time.sleep(1)