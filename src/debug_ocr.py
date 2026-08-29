import os
from pathlib import Path

import pymupdf
from dotenv import load_dotenv

from src.ocr_engine.tesseract_engine import TesseractEngine
from src.path_resolver import get_tesseract_data_path
from src.pdf_overlayer import overlay_text

load_dotenv()

ocr_engine = TesseractEngine(tess_data_path=str(get_tesseract_data_path()))
debug_pdf: str = os.environ["DEBUG_PDF_PATH"]
pdf = pymupdf.open(filename=debug_pdf)

for page_number, text in ocr_engine.process_doc(pdf, return_with_boxes=True):
     overlay_text(pdf[page_number], text) # pyright: ignore[reportArgumentType]

output_path = Path(debug_pdf).parent / f"{Path(debug_pdf).stem}_overlaid.pdf"
pdf.save(filename=str(output_path))
pdf.close()