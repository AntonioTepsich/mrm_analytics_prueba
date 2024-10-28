import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import io
import cv2
import re
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def crop_box(image, left=0, right=0, top=0, bottom=0, display_image=False):
    """Recorta los márgenes de una imagen."""
    width, height = image.size
    left_margin = width * left
    top_margin = height * top
    right_margin = width * (1 - right)
    bottom_margin = height * (1 - bottom)
    if display_image:
        image.crop((left_margin, top_margin, right_margin, bottom_margin)).show()
    return image.crop((left_margin, top_margin, right_margin, bottom_margin))


def first_page(cropped_img, page_num):
    cropped_width, cropped_height = cropped_img.size

    # Definir los factores de recorte para las subimágenes
    middle_height_factor = 0.378  # Proporción del alto para la parte media (35% de la altura total)
    top_height_factor = 0.22  # Proporción del alto para la parte superior (30% de la altura total)
    left_width_factor = 0.5  # Proporción del ancho para la parte izquierda (50%)

    # Definir las coordenadas de las subimágenes utilizando los factores
    # Parte Superior Izquierda
    top_left = cropped_img.crop((
        0,  # Desde el borde izquierdo
        0,  # Desde el borde superior
        cropped_width * left_width_factor,  # Hasta la mitad del ancho (izquierda)
        cropped_height * top_height_factor  # Hasta el 22% del alto (parte superior)
    ))

    # Parte Superior Derecha
    top_right = cropped_img.crop((
        cropped_width * left_width_factor,  # Desde la mitad del ancho (derecha)
        0,  # Desde el borde superior
        cropped_width,  # Hasta el borde derecho
        cropped_height * top_height_factor  # Hasta la mitad del alto (parte superior)
    ))

    # Mitad 
    middle = cropped_img.crop((
        0,  # Desde el borde izquierdo
        cropped_height * top_height_factor,  # Desde la mitad del alto
        cropped_width,  # Hasta el borde derecho
        cropped_height * middle_height_factor  # Hasta el 35% del alto de la imagen
    ))

    # case_no = img_low_dpi.crop((
    #     width_low*0.5,  # Desde el borde izquierdo
    #     height_low * 0.36,  # Desde la mitad del alto
    #     width_low* 0.94,  # Hasta el borde derecho
    #     height_low * 0.385  # Hasta el 35% del alto de la imagen
    # ))

    # Mitad Inferior Izquierda
    bottom_left = cropped_img.crop((
        0,  # Desde el borde izquierdo
        cropped_height * middle_height_factor,  # Desde el 30% del alto (parte inferior)
        cropped_width * 0.455,  # Hasta la mitad del ancho (izquierda)
        cropped_height  # Hasta el borde inferior
    ))

    # Mitad Inferior Derecha
    bottom_right = cropped_img.crop((
        cropped_width * 0.47,  # Desde la mitad del ancho (derecha)
        cropped_height * middle_height_factor,  # Desde el 30% del alto (parte inferior)
        cropped_width,  # Hasta el borde derecho
        cropped_height  # Hasta el borde inferior
    ))

    # Mostrar las subimágenes recortadas (para verificar visualmente)
    # top_left.show()
    # top_right.show()
    # middle.show()
    # case_no.show()
    # bottom_left.show()
    # bottom_right.show()

    # Extraer texto con OCR de cada parte usando Tesseract con parámetros personalizados
    custom_config = r'--oem 1 --psm 3'

    # Parte Superior Izquierda
    text_top_left = pytesseract.image_to_string(top_left, config=custom_config, lang="eng")
    print(f"Página {page_num + 1} - Parte Superior Izquierda:\n{text_top_left}\n")

    # Parte Superior Derecha
    text_top_right = pytesseract.image_to_string(top_right, config=custom_config, lang="eng")
    print(f"Página {page_num + 1} - Parte Superior Derecha:\n{text_top_right}\n")

    # Mitad Inferior Izquierda
    text_bottom_left = pytesseract.image_to_string(bottom_left, config=custom_config, lang="eng")
    print(f"Página {page_num + 1} - Mitad Inferior Izquierda:\n{text_bottom_left}\n")

    text_middle = pytesseract.image_to_string(middle, config=custom_config, lang="eng")
    print(f"Página {page_num + 1} - Mitad Inferior Izquierda:\n{text_middle}\n")

    # text_case_no = pytesseract.image_to_string(case_no, config=custom_config, lang="eng")
    # print(f"Página {page_num + 1} - Case No:\n{text_case_no}\n")

    # Mitad Inferior Derecha
    text_bottom_right = pytesseract.image_to_string(bottom_right, config=custom_config, lang="eng")
    print(f"Página {page_num + 1} - Mitad Inferior Derecha:\n{text_bottom_right}\n")



def detect_and_crop_margins(image):
    """Detectar líneas horizontales y verticales largas y recortar la imagen, manteniendo la parte superior."""
    # Convertir la imagen de PIL a OpenCV en escala de grises
    open_cv_image = np.array(image.convert('L'))  # 'L' convierte la imagen a escala de grises
    gray = open_cv_image

    # Aplicar detección de bordes
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # ----------------- Detectar Líneas Verticales -----------------
    min_line_length_vertical = gray.shape[0] * 0.8  # Longitud mínima de las líneas verticales (80% de la altura)
    max_line_gap_vertical = 10
    vertical_lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=min_line_length_vertical, maxLineGap=max_line_gap_vertical)

    left_bound, right_bound = None, None

    if vertical_lines is not None:
        for line in vertical_lines:
            x1, y1, x2, y2 = line[0]
            # Verificar si la línea es vertical (x1 aproximadamente igual a x2)
            if abs(x1 - x2) < 10:
                if left_bound is None or x1 < left_bound:
                    left_bound = x1
                if right_bound is None or x1 > right_bound:
                    right_bound = x1

    # ----------------- Detectar Líneas Horizontales -----------------
    min_line_length_horizontal = gray.shape[1] * 0.8  # Longitud mínima de las líneas horizontales (80% del ancho)
    max_line_gap_horizontal = 10
    horizontal_lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=min_line_length_horizontal, maxLineGap=max_line_gap_horizontal)

    bottom_bound = None

    if horizontal_lines is not None:
        for line in horizontal_lines:
            x1, y1, x2, y2 = line[0]
            # Verificar si la línea es horizontal (y1 aproximadamente igual a y2)
            if abs(y1 - y2) < 10:
                if bottom_bound is None or y1 < bottom_bound:
                    bottom_bound = y1

    # ----------------- Aplicar el Recorte Basado en las Líneas Detectadas -----------------
    if left_bound is not None and right_bound is not None and bottom_bound is not None:
        margin_v = -18  # Margen adicional para evitar cortar contenido relevante
        margin_h = 60  # Margen adicional para evitar cortar contenido relevante
        # Calcular los límites de recorte, asegurándonos de que no salgan de la imagen
        left_crop = max(0, left_bound - margin_v)
        right_crop = min(gray.shape[1], right_bound + margin_v)
        bottom_crop = max(0, bottom_bound - margin_h)

        # Verificar si los límites de recorte tienen sentido
        if left_crop < right_crop and bottom_crop > 0:
            cropped_image = gray[:bottom_crop, left_crop:right_crop]  # Recortar desde la parte superior hasta la línea horizontal detectada
            if cropped_image.size == 0:
                print("Recorte fallido, la imagen resultante está vacía.")
                return image  # Devuelve la imagen original si el recorte falla
            # Convertir la imagen recortada de nuevo a PIL (escala de grises)
            cropped_image_pil = Image.fromarray(cropped_image)
            return cropped_image_pil
        else:
            print("Recorte no válido, los límites de recorte son incorrectos.")
            return image
    else:
        print("No se encontraron líneas apropiadas para recortar.")
        return image

def extract_text_with_ocr(pdf_path):
    # Abre el PDF con PyMuPDF (fitz)
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Renderizar la página a una imagen con mayor DPI
        pix = page.get_pixmap(dpi=50)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert('L')  # Convertir la imagen a escala de grises al cargarla

        # Aplicar el recorte de márgenes
        cropped_img = detect_and_crop_margins(img)
        cropped_img.show()

        # Extraer texto con OCR de la imagen recortada
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(cropped_img, config=custom_config, lang="eng")

        # Eliminar "///" del final si está presente
        if text.strip().endswith("///"):
            text = text.strip()[:-3].rstrip()

        # Eliminar "PAGE {nro}" del final si está presente
        text = re.sub(r"PAGE \d+$", "", text.strip(), flags=re.IGNORECASE)

        # Dividir el texto en líneas
        lines = text.splitlines()

        # ------------------ Filtrar Pies de Página Potenciales ------------------
        # Crear una lista solo con líneas significativas (sin contar las líneas vacías)
        significant_lines = [line for line in lines if line.strip()]

        # Verificar las últimas 2 o 3 líneas significativas para determinar si deben eliminarse
        lines_to_check = min(3, len(significant_lines))
        lines_to_remove = 0

        for i in range(1, lines_to_check + 1):
            line = significant_lines[-i].strip()
            # Verificar si la línea solo tiene números, guiones o puntos
            if re.match(r'^[\d\-.]+$', line):
                lines_to_remove += 1
            else:
                break  # Si una línea no cumple con la condición, detenemos la eliminación

        # Eliminar las últimas líneas si cumplen con la condición
        if lines_to_remove > 0:
            lines = lines[:-(lines_to_remove + sum(1 for l in lines[-lines_to_remove:] if not l.strip()))]

        # Unir las líneas nuevamente
        filtered_text = "\n".join(lines)
        print(f"Página {page_num + 1}:\n{filtered_text}\n")


        break


# Llamar a la función con la ruta del archivo PDF
extract_text_with_ocr("tests/test2.pdf")
