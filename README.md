### Purpose
"give me the .exe".

I wanted something that OCR-ed PDFs with text overlay, but ocrmypdf was a CLI interface. The existing GUI wrappers that I could find required some amount of setup and external dependencies.

I took the opportunity to learn about tkinter and the basics of event-driven programming.

### Technologies
tkinter, pymupdf, tesserocr

### Architecture
Encapsulation and single responsibility principle (orchestrator.py and GUI.py). Multithreading to keep GUI responsive and batch processing for faster OCR speeds.

### Installation
Download the .zip from releases, unzip and click the executable.