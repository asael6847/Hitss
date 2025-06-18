# src/interactions/extract_data.py

import allure
from playwright.sync_api import Locator

class ExtractData:
    def __init__(self, page):
        self.page = page

    @allure.step("Extraer el título y la descripción específica de la sección")
    def from_content_row(self, row_locator: Locator):
        """
        Extrae el título y la descripción de un localizador de fila (et_pb_row_N).
        Busca el texto dentro de los div.et_pb_text_inner correspondientes.
        """
        extracted_info = {
            "title": None,
            "description": None
        }

        try:
            # Encuentra el div.et_pb_text_inner que contiene el título (generalmente el primero con strong)
            # Ejemplo para CRM: <div class="et_pb_text_inner"><p><strong>CRM</strong></p></div>
            # Usamos :has(strong) para apuntar específicamente al div que contiene el strong del título.
            title_text_inner = row_locator.locator(".et_pb_text_inner:has(strong)").first
            if title_text_inner.is_visible():
                extracted_info["title"] = title_text_inner.text_content().strip()
            
            # Encuentra el div.et_pb_text_inner que contiene la descripción.
            # Este es usualmente el segundo div.et_pb_text_inner en la columna de texto.
            # ".et_pb_text_inner" selecciona todos los elementos con esa clase dentro de row_locator.
            # .nth(1) selecciona el segundo elemento (índice 1) de esos encontrados.
            description_text_inner = row_locator.locator(".et_pb_text_inner").nth(1)
            if description_text_inner.is_visible():
                extracted_info["description"] = description_text_inner.text_content().strip()

        except Exception as e:
            print(f"Advertencia: No se pudo extraer información detallada del elemento en la fila. Error: {e}")

        return extracted_info