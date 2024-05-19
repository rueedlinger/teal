# Teal - A Convenient REST API for Working with PDFs

**Teal** is a versatile and user-friendly API designed to simplify working with PDF documents. Whether you're a
developer looking to automate PDF processing or integrate PDF functionalities into your existing workflow, Teal provides
a seamless and efficient solution.

## Understanding Different Types of PDFs

**Digitally Created PDFs:**

- Created using software like Microsoft Word or Excel, or via the "print" function within applications.
- Contains text and images with electronic character designation.
- Text and images can be easily edited, searched, and manipulated.

**Image-only PDFs:**

- Generated from scanned hard copy documents or images.
- Content is locked in a snapshot-like image without a text layer.
- Not searchable or editable without OCR (Optical Character Recognition).

**Searchable PDFs:**

- Result from applying OCR to scanned or image-based documents.
- Have a text layer added underneath the image layer, making them fully searchable.
- Text can be selected, copied, and marked up like in original documents.

## Key Features

- Digitize documents to searchable or archivable PDF (PDF/A).
- Extract metadata, text, and tables as structured data.
- Convert different document types to PDF.
- Convert PDFs to PDF/A.
- Check PDF/A compliance.

## Getting Started

Here's a quick example of how easy it is to work with Teal:

To begin using Teal, check out our detailed documentation which covers installation, usage examples, and comprehensive
guides on all API features.

## Deployment

tbd

## API

- see [API.md](doc/API.md)

## Libraries Used in Teal

**Teal** uses other open-source libraries and provides this functionality through convenient APIs.

| Feature                                           | Library                 |
|---------------------------------------------------|-------------------------|
| Extract text from PDFs                            | pypdfium2               |
| Extract text from scanned PDFs (OCR)              | pytesseract             |
| Extract tables from PDFs                          | camelot                 |
| Convert PDF to PDF/A (with OCR when no text)      | ocrmypdf                |
| Convert Office documents to PDF                   | libreoffice             |
| PDF/A validation                                  | veraPDF                 |
| Extract meta data from PDF                        | **not yet implemented** |
| Process documents from a remote repository (HTTP) | **not yet implemented** |



