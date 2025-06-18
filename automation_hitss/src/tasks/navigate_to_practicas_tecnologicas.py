# src/tasks/navigate_to_practicas_tecnologicas.py

from src.abilities.browse_the_web import BrowseTheWeb
from src.interactions.take_screenshot import TakeScreenshot
from src.actors.actor import Actor
from src.interactions.extract_data import ExtractData # ¡Importa la nueva clase de scraping!
import time
import allure
import csv # Para guardar los datos en formato CSV
import os # Para operaciones con el sistema de archivos (crear directorio, etc.)

class NavigateToPracticasTecnologicas:

    def __init__(self):
        self._request = None
        # Define el directorio donde se guardarán los archivos CSV
        self.output_dir = "extracted_data"
        # Crea el directorio si no existe. 'exist_ok=True' evita un error si ya existe.
        os.makedirs(self.output_dir, exist_ok=True) 
        # Define la ruta completa para el archivo CSV donde se guardarán los datos
        self.csv_file_path = os.path.join(self.output_dir, "practicas_tecnologicas_data.csv")

    def with_request(self, request):
        self._request = request
        return self

    @allure.step("Navegar a 'Prácticas Tecnológicas' y extraer contenido de filas")
    def perform_as(self, actor):
        page = actor.ability_to(BrowseTheWeb).page
        # Instancia la clase para extraer datos, pasándole el objeto 'page' de Playwright
        data_extractor = ExtractData(page) 

        # Inicializa el archivo CSV con encabezados si no existe o está vacío
        # Esto asegura que los encabezados se escriban solo una vez.
        if not os.path.exists(self.csv_file_path) or os.stat(self.csv_file_path).st_size == 0:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Fila_N", "Titulo", "Descripcion"]) # Encabezados de las columnas del CSV

        with allure.step("Clic en 'Soluciones' y captura inicial"):
            page.locator("#menu-global-hitss").get_by_text("Soluciones").click()
            time.sleep(0.5) 

            actor.attempts_to(
                TakeScreenshot.of_the_page("despues_de_soluciones.png"),
                request=self._request 
            )
            print("Captura tomada después de hacer clic en 'Soluciones'.")


        with allure.step("Clic en 'PRÁCTICAS TECNOLÓGICAS'"):
            # Selector más específico para el enlace "PRÁCTICAS TECNOLÓGICAS"
            practicas_tecnologicas_link = page.locator("nav.et-menu-nav ul#menu-global-hitss li a[href*='practicas-tecnologicas']").filter(has_text="PRÁCTICAS TECNOLÓGICAS")
            practicas_tecnologicas_link.click()
            time.sleep(0.5) 


        # Bucle para iterar sobre las filas de contenido et_pb_row_N
        # Itera desde la fila 3 (donde empieza CRM) hasta la fila 17.
        # Es crucial que estas filas existan y sean visibles en tu página.
        start_row_number = 3
        end_row_number = 17

        for n in range(start_row_number, end_row_number + 1):
            # Selector CSS para la fila actual et_pb_row_N
            row_selector = f"div.et_pb_row.et_pb_row_{n}.et_pb_equal_columns.et_had_animation"

            with allure.step(f"Desplazarse a la fila et_pb_row_{n}, tomar captura y extraer datos"):
                print(f"Intentando interactuar con el selector: {row_selector}")
                try:
                    current_row_locator = page.locator(row_selector)

                    # Espera hasta 10 segundos para que la fila sea visible
                    current_row_locator.wait_for(state="visible", timeout=10000)
                    # Desplaza la página para que la fila esté en la vista
                    current_row_locator.scroll_into_view_if_needed()
                    time.sleep(2) # Pausa para asegurar que el scroll se complete y el elemento esté estable

                    # --- REALIZA EL SCRAPING: Llama al método de la clase ExtractData ---
                    extracted_data = data_extractor.from_content_row(current_row_locator)
                    print(f"Datos extraídos de et_pb_row_{n}: {extracted_data}")

                    # --- GUARDA LOS DATOS EN EL ARCHIVO CSV ---
                    with open(self.csv_file_path, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        # Escribe los datos de la fila actual en el CSV
                        writer.writerow([n, extracted_data.get("title", ""), extracted_data.get("description", "")])

                    # --- ADJUNTA LOS DATOS AL REPORTE ALLURE PARA VISUALIZACIÓN ---
                    allure.attach(
                        f"Fila {n}:\nTitulo: {extracted_data.get('title', 'N/A')}\nDescripción: {extracted_data.get('description', 'N/A')}",
                        name=f"Datos_et_pb_row_{n}",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    # Genera un nombre para el archivo de captura basado en el título extraído
                    section_name_for_screenshot = extracted_data.get("title", f"fila_{n}").replace(" ", "_").replace("/", "-").replace("&", "and")
                    if len(section_name_for_screenshot) > 50: # Limita el nombre si es muy largo
                        section_name_for_screenshot = section_name_for_screenshot[:50] + "..."

                    # --- TOMA LA CAPTURA DE PANTALLA ---
                    actor.attempts_to(
                        TakeScreenshot.of_the_page(f"captura_fila_et_pb_row_{n}_{section_name_for_screenshot}.png"),
                        request=self._request
                    )
                    print(f"Captura tomada para la fila: '{section_name_for_screenshot}' (et_pb_row_{n}).")

                except Exception as e:
                    print(f"ERROR: No se pudo interactuar o capturar/extraer de la fila {row_selector}: {e}")
                    # Continúa con la siguiente iteración incluso si una falla

        time.sleep(1) # Pausa final
        # page.pause() # Descomenta para pausar el navegador al final (solo para depuración)