from .base_extractor import BaseExtractor
from services.utils.ocr_utils import convert_pdf_page_to_image, crop_box,apply_ocr_to_image
import fitz
import cv2
import numpy as np
from PIL import Image
import re
import time

class Test2Extractor(BaseExtractor):
    def __init__(self, analyze_first_page=False):
        super().__init__(analyze_first_page)
        self.first_page_config = r'--oem 3 --psm 3'
        self.other_pages_config = r'--oem 3 --psm 6'

    def _process_pdf(self, temp_pdf_path: str, analyze_first_page: bool) -> str:
        combined_text = []
        doc = fitz.open(temp_pdf_path)

        if analyze_first_page:
            first_page_text = self._extract_first_page(doc)
            combined_text.append(first_page_text)

        other_pages_text = self._extract_other_pages(doc)
        combined_text.extend(other_pages_text)

        return "\n".join(combined_text)

    def _extract_first_page(self, doc) -> str:

        img = convert_pdf_page_to_image(doc, 0, dpi=70)
        img_prepared = self._prepare_image_for_ocr(img)

        text = apply_ocr_to_image(img_prepared, config=self.first_page_config, lang="eng")
        case_no = self._extract_case_number(text)

        return case_no

    def _extract_case_number(self, text: str) -> str:
        pattern = r'\d{2}[A-Z]{2}\s[A-Z]{2}\s\d{5}'
        matches = re.findall(pattern, text)
        return f"Case No.: {matches[0] if matches else 'No Case No. found'}\n"

    def _extract_other_pages(self, doc) -> list:
        combined_text = []

        for page_num in range(1, len(doc)):
            img = convert_pdf_page_to_image(doc, page_num, dpi=200)
            cropped_img = self._detect_and_crop_margins(img)

            text = apply_ocr_to_image(cropped_img, config=self.other_pages_config, lang="eng")
            cleaned_text = self._clean_irrelevant_info(text)
            combined_text.append(cleaned_text)

        return combined_text

    def _prepare_image_for_ocr(self, img) -> np.ndarray:
        gray_image = np.array(img.convert('L'))
        blurred = cv2.bilateralFilter(gray_image, d=6, sigmaColor=15, sigmaSpace=15)
        _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def _detect_and_crop_margins(self, image: Image) -> Image:
        gray = np.array(image.convert('L'))
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        left_bound, right_bound = self._detect_vertical_lines(edges, gray)
        bottom_bound = self._detect_horizontal_lines(edges, gray)

        return self._crop_image(gray, left_bound, right_bound, bottom_bound)

    def _detect_vertical_lines(self, edges: np.ndarray, gray: np.ndarray):
        min_line_length_vertical = gray.shape[0] * 0.8
        vertical_lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=min_line_length_vertical, maxLineGap=10)

        left_bound, right_bound = None, None
        if vertical_lines is not None:
            for line in vertical_lines:
                x1, _, x2, _ = line[0]
                if abs(x1 - x2) < 10:
                    left_bound = min(left_bound, x1) if left_bound is not None else x1
                    right_bound = max(right_bound, x1) if right_bound is not None else x1

        return left_bound, right_bound

    def _detect_horizontal_lines(self, edges: np.ndarray, gray: np.ndarray):
        min_line_length_horizontal = gray.shape[1] * 0.8
        horizontal_lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=min_line_length_horizontal, maxLineGap=10)

        bottom_bound = None
        if horizontal_lines is not None:
            for line in horizontal_lines:
                _, y1, _, y2 = line[0]
                if abs(y1 - y2) < 10:
                    bottom_bound = min(bottom_bound, y1) if bottom_bound is not None else y1

        return bottom_bound

    def _crop_image(self, gray: np.ndarray, left_bound, right_bound, bottom_bound):
        if left_bound is not None and right_bound is not None and bottom_bound is not None:
            margin_v = -18
            margin_h = 60
            left_crop = max(0, left_bound - margin_v)
            right_crop = min(gray.shape[1], right_bound + margin_v)
            bottom_crop = max(0, bottom_bound - margin_h)

            if left_crop < right_crop and bottom_crop > 0:
                cropped_image = gray[:bottom_crop, left_crop:right_crop]
                if cropped_image.size == 0:
                    return Image.fromarray(gray)
                return Image.fromarray(cropped_image)

        return Image.fromarray(gray)

    def _clean_irrelevant_info(self, text: str) -> str:
        text = re.sub(r"///$", "", text.strip())
        text = re.sub(r"PAGE \d+$", "", text.strip(), flags=re.IGNORECASE)

        lines = text.splitlines()
        significant_lines = [line for line in lines if line.strip()]

        lines_to_remove = 0
        lines_to_check = min(3, len(significant_lines))

        for i in range(1, lines_to_check + 1):
            line = significant_lines[-i].strip()
            if re.match(r'^[\d\-.]+$', line):
                lines_to_remove += 1
            else:
                break

        if lines_to_remove > 0:
            lines = lines[:-(lines_to_remove + sum(1 for l in lines[-lines_to_remove:] if not l.strip()))]

        return "\n".join(lines)