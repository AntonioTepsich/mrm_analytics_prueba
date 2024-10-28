from PIL import Image
import pytesseract
import io

def apply_ocr_to_image(image, config=r'--oem 3 --psm 6', lang='eng'):
    """Aplica OCR a una imagen dada."""
    return pytesseract.image_to_string(image, config=config, lang=lang)

def convert_pdf_page_to_image(doc, page_num, dpi=150):
    """Convierte una página del PDF en una imagen de alta resolución."""
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return img

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
