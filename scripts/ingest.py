from pathlib import Path
import fitz  # PyMuPDF
import re

RAW_DIR = Path("data/raw_papers")
OUT_DIR = Path("data/extracted_text")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract raw text from a PDF, page by page.
    Preserves structure; no aggressive cleaning.
    """
    with fitz.open(pdf_path) as doc:
        pages = [page.get_text("text") for page in doc]

    return "\n".join(pages)


# def basic_cleanup(text: str) -> str:
#     """
#     Very conservative cleanup:
#     - remove empty lines
#     - normalize whitespace
#     """
#     cleaned_lines = []

#     for line in text.splitlines():
#         line = line.strip()
#         if not line:
#             continue
#         cleaned_lines.append(line)

#     return "\n".join(cleaned_lines)

def normalize_text(text: str) -> str:
    import re

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    merged = []
    buffer = ""

    for line in lines:
        if buffer:
            if not re.search(r"[.:;?!]$", buffer):
                # safer hyphen fix
                if buffer.endswith("-") and line and line[0].islower():
                    buffer = buffer[:-1] + line
                else:
                    buffer = buffer + " " + line
            else:
                merged.append(buffer)
                buffer = line
        else:
            buffer = line

    if buffer:
        merged.append(buffer)

    return "\n\n".join(merged)




def main() -> None:
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDFs found in data/raw_papers/")
        return

    for pdf_path in pdf_files:
        print(f"📄 Processing: {pdf_path.name}")

        raw_text = extract_text_from_pdf(pdf_path)
        clean_text = normalize_text(raw_text)

        if not clean_text.strip():
            print(f"⚠️ Warning: No text extracted from {pdf_path.name}")
            continue

        out_path = OUT_DIR / f"{pdf_path.stem}.txt"
        out_path.write_text(clean_text, encoding="utf-8")

        print(f"✅ Saved: {out_path}")


if __name__ == "__main__":
    main()
