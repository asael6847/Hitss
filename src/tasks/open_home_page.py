from src.abilities.browse_the_web import BrowseTheWeb

class OpenHomePage:
    def __init__(self,url):
        self.url = url
    
    def perform_as(self,actor):
        page = actor.ability_to(BrowseTheWeb).page
        page.goto(self.url)