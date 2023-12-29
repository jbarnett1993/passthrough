import fitz  # PyMuPDF

def create_toc_page(doc, titles_and_pages):
    """
    Create a TOC page with given titles and their starting page numbers.
    """
    toc_page = doc.new_page(width=612, height=792)  # Create a new page for TOC
    toc_page.insert_text((72, 72), "Table of Contents", fontsize=16, fontname="helv")

    y_position = 100
    for title, page in titles_and_pages:
        toc_text = f"{title} - Start on Page {page}"
        toc_page.insert_text((72, y_position), toc_text, fontsize=12, fontname="helv")
        y_position += 20

def merge_pdfs(paths, output):
    doc = fitz.open()  # Create a new PDF

    # List to hold titles and their starting page numbers
    titles_and_pages = []
    current_page = 1  # Start from 1 to account for the TOC page

    for path in paths:
        pdf_doc = fitz.open(path)
        title = path.rsplit('/', 1)[-1].replace('.pdf', '')
        titles_and_pages.append((title, current_page))

        doc.insert_pdf(pdf_doc)
        current_page += len(pdf_doc)

    # Create TOC page
    create_toc_page(doc, titles_and_pages)

    # Save the merged PDF
    doc.save(output)
    doc.close()

# Example usage
paths = ['pdf1.pdf', 'pdf2.pdf', 'pdf3.pdf']  # Replace with your actual file names
merge_pdfs(paths, 'merged_with_toc.pdf')