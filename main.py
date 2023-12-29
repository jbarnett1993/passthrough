import fitz  # PyMuPDF

def create_toc_content(titles_and_pages):
    """
    Create a TOC content as a single page PDF.
    """
    # Create a new PDF for TOC content
    toc_doc = fitz.open()
    toc_page = toc_doc.new_page(width=612, height=792)  # Standard letter size

    # Add TOC title
    toc_page.insert_text((72, 72), "Table of Contents", fontsize=16, fontname="helv")

    # Add TOC entries
    y_position = 100
    for title, page in titles_and_pages:
        toc_text = f"{title} - Start on Page {page}"
        toc_page.insert_text((72, y_position), toc_text, fontsize=12, fontname="helv")
        y_position += 20

    return toc_doc

def merge_pdfs(paths, output):
    merged_doc = fitz.open()  # Create a new PDF for the merged document

    # List to hold titles and their starting page numbers
    titles_and_pages = []
    current_page = 2  # Start from 2 as the first page will be the TOC

    for path in paths:
        pdf_doc = fitz.open(path)
        title = path.rsplit('/', 1)[-1].replace('.pdf', '')
        titles_and_pages.append((title, current_page))

        merged_doc.insert_pdf(pdf_doc)
        current_page += len(pdf_doc)

    # Create TOC content
    toc_doc = create_toc_content(titles_and_pages)

    # Insert TOC as the first page
    merged_doc.insert_pdf(toc_doc, to_page=0)

    # Save the merged PDF
    merged_doc.save(output)
    merged_doc.close()

# Example usage
paths = ['pdf1.pdf', 'pdf2.pdf', 'pdf3.pdf']  # Replace with your actual file names
merge_pdfs(paths, 'merged_with_toc.pdf')