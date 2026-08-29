"""
Contains all the relevant functions for tesseract's OCR pipeline: preprocessing, text extraction and document orchestration.
"""

import os
import threading
from _thread import _local
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait

import cv2
import numpy as np
from PIL import Image
from pymupdf import Document, Page
from tesserocr import PyTessBaseAPI  # pyright: ignore[reportMissingImports]

from src.ocr_engine.base import OCREngine
from src.ocr_engine.preprocessing_utils import deskew_image, page_to_numpy


# we pass OCREngine as a parameter, meaning that
#  TesseractEngine inherits its ABC methods
class TesseractEngine(OCREngine):
    def __init__(self, tess_data_path: str):
        self._tess_data_path: str = tess_data_path
        self._thread_local: _local = (
            threading.local()
        )  # namespace for each individual thread

    def _get_api(self):
        if not hasattr(self._thread_local, "api"):
            try:
                # access the api attribute on the threading.local object\
                # okay I honestly don't know what that means but I think
                #  we can set the API interface as an attr
                self._thread_local.api = PyTessBaseAPI(path=self._tess_data_path)  # pyright: ignore[reportAttributeAccessIssue]
            except Exception:  # noqa
                raise RuntimeError("Failed to initialize PyTessBaseAPI")
        return self._thread_local.api  # so that methods can actually access it

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        """
        Args:
            img(np.ndarray): OpenCV image as numpy array
        Returns:
            Preprocessed image (BGR) as numpy array
        """

        # pylint: disable=E1101

        # we skip greyscale because pymupdf already loads the pixmap as
        #  grayscale

        img = deskew_image(img)

        denoised = cv2.bilateralFilter(img, 9, 75, 75)

        # THRESH_BINARY turns every pixel below the threshold white, and every
        #  pixel above the threshold black.
        # THRESH_OTSU figures out what the threshold value should be by seeing
        #  where the variance between two groups is minimized/maximized.
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        return binary

    def process_page(self, page: Page):
        """
        Extracts text from a single page using a pre-existing tesseract API instance. Also includes pre-processing.

        Args:
            img(np.ndarray): The image's numpy array

        Returns:
            A string containing the contents of the page.
        """

        # convert img to numpy array
        img_np = page_to_numpy(page)

        # preprocessing
        preprocessed = self._preprocess(img_np)

        # convert to PIL Image
        pil_img = Image.fromarray(preprocessed)

        # get the API (should already be initialized)
        api = self._get_api()

        # pass the PIL Image into the engine
        api.SetImage(pil_img)

        # run the engine and extract the text
        text = api.GetUTF8Text()

        return text

    def process_doc(self, doc: Document):
        """
        Lazily streams tuples containing the page number and the text contents of a pdf.

        Args:
            pdf(pymupdf.Document): The pdf's structure (not the entire pdf!) loaded into memory
        Returns:
            A generator object that returns Tuples sequentially when called.
            The tuple contains the page number, and the page contents respectively.
            Example: [0, "The first page"]
        """

        # initialize the api
        if self._tess_data_path is None:
            raise RuntimeError(
                "tesseract.tesseract_orchestrator.py received None in TESS_DATA_PATH"
            )

        self._get_api()
        workers = 1
        cpu_count: int | None = os.cpu_count()
        if cpu_count is not None:
            workers = cpu_count - 1
        # we want to implement a sliding window.
        # we need to track which tasks are still pending, and keep the window full.
        pending: dict[int, Future[str]] = {}
        future_to_page: dict[Future[str], int] = {}
        page_idx: int = 0
        next_in_line: int = 0
        results: dict[int, str] = {}
        with ThreadPoolExecutor(max_workers=workers) as executor:
            while page_idx < len(doc):
                # fill the thread pool up with futures
                while len(pending) < workers and page_idx < len(doc):
                    pending[page_idx] = executor.submit(
                        self.process_page, doc[page_idx]
                    )
                    future_to_page[pending[page_idx]] = page_idx
                    page_idx += 1

                while future_to_page:
                    done, _ = wait(fs=pending.values(), return_when=FIRST_COMPLETED)

                    # get back the results using a reverse dict
                    for future in done:
                        future_number: int = future_to_page[future]
                        results[future_number] = (
                            future.result()
                        )  # this is instant because its done
                        del future_to_page[future]  # it has served its purpose
                        del pending[future_number]

                    for key in sorted(results.keys()):
                        if key == next_in_line:
                            yield (key, results[key])
                            del results[key]
                            next_in_line += 1
