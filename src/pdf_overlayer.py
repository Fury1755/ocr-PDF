from pymupdf import Page, Pixmap


def flatten_pdf(page: Page) -> Page:
    '''
    Flattens whatever PDF with previously overlaid text into a PDF with no text.
    '''

    # render the page into an image(pixmap)
    pix: Pixmap = page.get_pixmap(dpi=300)
    page.clean_contents()

    rect = page.rect # apparently we need this
    page.insert_image(rect, pixmap=pix)

    return page

def overlay_text(page: Page, text: list[tuple[str, tuple[int, int, int, int]]]) -> None:
    '''
    Overlays text on top of a page. Modifies the page by reference.

    Args: 
        page(pymupdf.Page): The page from that particular page
        text(list[tuple[str, tuple[int, int, int, int]]]): output from process_doc with coordinates (x1, y1, x2, y2)
    '''

    # first note that tesseract returns coordinates in pixels, while pymupdf calculates in per inches.
    # We have, in our pre-processing, selected a DPI of 300.
    # pymupdf measures the position in PDF points (72 points per inch).
    # To convert Tesseract coordinates to pymupdf points we multiply by 72/300.
    scale: float = 72/300

    # Tesseract y-coords go from top to bottom while pymupdf's go from bottom to top
    page_height = page.rect.height
    page_width = page.rect.width

    for word in text:
        # multiply the coordinates by the scale factor and flip the y-axes
        # note the order is also flipped
        x0: float = word[1][0]*scale
        y0: float= word[1][1]*scale
        x1: float = word[1][2]*scale
        y1: float = word[1][3]*scale
        assert x0<=x1
        assert y0<=y1
        raw_text = word[0]
        # for some reason, insert_textbox isn't working. We'll use insert_text instead.
        page.insert_text(point=(x0,(y1+y0)/2), text=raw_text, fontsize=(y1-y0), render_mode=3)