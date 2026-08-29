### Purpose
I wanted something that OCR-ed PDFs with text overlay, but ocrmypdf was a CLI interface. The existing GUI wrappers, however fancy, also required some amount of setup and external dependencies.

In other words, there was no foolproof download for dummies like me. "give me the .exe".

Although I took the opportunity to learn about tkinter and the basics of event-driven programming, it would be shameful to call this a portfolio project.

### Technologies
tkinter, pymupdf, tesserocr 

### Architecture
Encapsulation and single responsibility principle (orchestrator.py and GUI.py). Multithreading to keep GUI responsive and batch processing for faster OCR speeds.

### Installation
Are you serious? Download the folder from releases, unzip and click the executable!