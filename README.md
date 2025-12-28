# minimal-rag

## ⚙️ Ingestion Pipeline

The ingestion process follows these steps:

1. **PDF Loading**
   - PDFs are loaded using PyMuPDF (fitz)

2. **Page-wise Text Extraction**
   - Text is extracted page by page to preserve document order

3. **Text Cleanup**
   - Removes empty lines
   - Removes standalone page numbers
   - Preserves legitimate hyphenated scientific terms
   - Ensures full sentence continuity

4. **Output**
   - One clean `.txt` file per paper
   - UTF-8 encoded
   - Readable end-to-end by humans and LLMs