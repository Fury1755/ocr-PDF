"""
An abstract base class that contains an interface, allowing us to swap out different OCR models easily
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator

import numpy as np
from pymupdf import Document, Page


class OCREngine(ABC):
    """
    Each engine handles its own preprocessing, document processing and page extraction.
    """

    @abstractmethod
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def process_doc(self, doc: Document) -> Iterator[tuple[int, str]]:
        pass

    @abstractmethod
    def process_page(self, page: Page) -> str:
        pass
