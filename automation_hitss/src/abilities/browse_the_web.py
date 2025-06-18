# src/abilities/browse_the_web.py

from playwright.sync_api import Page

class BrowseTheWeb:
    """
    Habilidad que permite al Actor interactuar con una página web
    utilizando Playwright.
    """
    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def with_(page: Page):
        """
        Método de clase para crear una instancia de BrowseTheWeb con una página dada.
        Esto permite una sintaxis más fluida: BrowseTheWeb.with_(page)
        """
        return BrowseTheWeb(page)

    def get_page(self) -> Page:
        """
        Obtiene la instancia de la página Playwright asociada a esta habilidad.
        """
        return self.page