from pathlib import Path

import pymupdf

from src.ocr_engine.tesseract_engine import TesseractEngine
from src.path_resolver import get_tesseract_data_path
from src.pdf_overlayer import overlay_text


class OCRController:
     def __init__(self, progress_callback, complete_callback, file_paths: list[str]):
          self.engine = None
          self.progress_callback = progress_callback
          self.complete_callback = complete_callback
          self.file_paths = file_paths
     
     def init_engine(self) -> TesseractEngine:
          # lazily load the TesseractEngine.
          # if we loaded it immediately, it would delay startup.
          self.engine = TesseractEngine(str(get_tesseract_data_path()))

          return self.engine

     def process_queue(self):
          self.engine = self.init_engine()

          for filename in self.file_paths:
               pdf = pymupdf.open(filename)
               for page_number, text in self.engine.process_doc(pdf, return_with_boxes=True):
                    overlay_text(pdf[page_number], text) # pyright: ignore[reportArgumentType]
                    if self.progress_callback: # satisfy type checker
                         assert type(page_number) is int
                         self.progress_callback(f"Page {page_number+1}/{len(pdf)} done.")

               output_path = Path(filename).parent / f"{Path(filename).stem}_overlaid.pdf"
               pdf.save(filename=str(output_path))
               pdf.close()
               if self.complete_callback:
                    self.complete_callback(f"PDF {Path(filename).stem} completed overlaying.")
               