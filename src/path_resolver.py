"""
This module resolves paths dynamically for compilation into an executable
"""

import sys
from pathlib import Path


def get_project_root() -> Path:
    """
    Returns root directory of project
    """

    if getattr(
        sys, "frozen", False
    ):  # frozen means that you've bundled your script; the python interpreter is bundled with the source code
    # sys._MEIPASS is a variable pyinstaller sets when the app is frozen.
    # it only exists upon bundling into an exe.
        return Path(sys._MEIPASS) # pyright: ignore[reportAttributeAccessIssue]
    
    else:
        return Path(__file__).parent.parent


def get_tesseract_data_path() -> Path:
    """
    Returns the path to the tessdata folder.
    """
    
    root: Path = get_project_root()
    return root/"Tesseract-OCR"/"tessdata"
