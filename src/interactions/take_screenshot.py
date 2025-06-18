# src/interactions/take_screenshot.py

import os
from playwright.sync_api import Page
from ..abilities.browse_the_web import BrowseTheWeb
import allure

class TakeScreenshot:
    """
    Una interacción que permite a un Actor tomar una captura de pantalla y adjuntarla
    automáticamente al reporte Allure.
    """
    def __init__(self, filename: str = "screenshot.png", directory: str = "screenshots"):
        self.filename = filename
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    @staticmethod # <--- ¡Asegúrate de que este decorador esté aquí!
    def of_the_page(filename: str = "screenshot.png", directory: str = "screenshots"):
        """
        Método de fábrica para crear una instancia de TakeScreenshot.
        Esto permite una sintaxis fluida como: TakeScreenshot.of_the_page(...)
        """
        return TakeScreenshot(filename, directory)

    def perform_as(self, actor, request=None): # Esta línea ya la habíamos corregido
        page: Page = actor.ability_to(BrowseTheWeb).page
        screenshot_path = os.path.join(self.directory, self.filename)

        page.screenshot(path=screenshot_path)
        print(f"Captura de pantalla guardada en: {screenshot_path}")

        try:
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=self.filename,
                    attachment_type=allure.attachment_type.PNG
                )
            print(f"Captura de pantalla '{self.filename}' adjuntada al reporte Allure.")
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo de captura en {screenshot_path}. ¿Fue guardado correctamente?")
        except Exception as e:
            print(f"ERROR: No se pudo adjuntar la captura al reporte Allure: {e}")