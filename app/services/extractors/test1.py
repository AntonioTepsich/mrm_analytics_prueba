from .base_extractor import BaseExtractor
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LAParams
import re


# Configuración de los parámetros de PDFMiner para la extracción
laparams = LAParams(
    char_margin=4.5,
    line_margin=0.5,
    word_margin=0.1,
    all_texts=True
)

# Patrones de expresiones regulares
number_paragraph_pattern = re.compile(r'^\d+$')
extra_spaces_pattern = re.compile(r' +')
title_pattern = re.compile(r'^[A-Z][A-Z0-9\s,.\'":\-]+$')

class Test1Extractor(BaseExtractor):
    def _process_pdf(self, temp_pdf_path: str, analyze_first_page: bool) -> str:
        extracted_paragraphs = []

        # Extraer todas las páginas del archivo PDF
        for page_num, page_layout in enumerate(extract_pages(temp_pdf_path, laparams=laparams)):
            self._process_page(page_layout, page_num, extracted_paragraphs)

        return "\n\n".join(extracted_paragraphs)

    def _process_page(self, page_layout, page_num: int, extracted_paragraphs: list):
        """Procesa cada página y extrae los párrafos de texto."""
        text_boxes = [element for element in page_layout if isinstance(element, LTTextBoxHorizontal)]
        paragraph_index = 0

        for box in text_boxes:
            filtered_text = self._process_text_box(box)

            if self._should_skip_paragraph(filtered_text, page_num, paragraph_index):
                paragraph_index += 1
                continue

            self._add_paragraph(filtered_text, extracted_paragraphs)
            paragraph_index += 1

    def _process_text_box(self, box) -> str:
        """Procesa un cuadro de texto, limpiando y filtrando el contenido."""
        text = box.get_text()
        lines = text.splitlines()

        # Reemplazar múltiples espacios por uno solo
        filtered_text = "\n".join(extra_spaces_pattern.sub(' ', line) for line in lines)

        return filtered_text

    def _should_skip_paragraph(self, filtered_text: str, page_num: int, paragraph_index: int) -> bool:
        """Determina si se debe omitir un párrafo."""
        return (
            not filtered_text.strip() or
            number_paragraph_pattern.match(filtered_text.strip()) or
            (page_num > 0 and paragraph_index == 0)
        )

    def _add_paragraph(self, filtered_text: str, extracted_paragraphs: list):
        """Agrega un párrafo a la lista, manejando títulos y concatenaciones."""
        stripped_text = filtered_text.strip()

        if len(stripped_text) < 50:
            extracted_paragraphs.append(stripped_text)
        else:
            self._handle_long_paragraph(stripped_text, extracted_paragraphs)

    def _handle_long_paragraph(self, stripped_text: str, extracted_paragraphs: list):
        """Maneja párrafos largos y su concatenación con párrafos previos."""
        if (
            extracted_paragraphs and 
            not extracted_paragraphs[-1].rstrip().endswith('.') and
            len(extracted_paragraphs[-1]) >= 50
        ):
            extracted_paragraphs[-1] += "\n" + stripped_text
        else:
            extracted_paragraphs.append(stripped_text)