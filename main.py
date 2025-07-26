import json
import os
import fitz  

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = []

    # Collect text with font sizes
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    if text:
                        font_sizes.append(s["size"])
                        headings.append((s["size"], text, page_num))

    # Sort font sizes (unique) to define hierarchy
    unique_sizes = sorted(set(font_sizes), reverse=True)
    title_font = unique_sizes[0]
    h1_font = unique_sizes[0]
    h2_font = unique_sizes[1] if len(unique_sizes) > 1 else unique_sizes[0]
    h3_font = unique_sizes[2] if len(unique_sizes) > 2 else unique_sizes[-1]

    # Detect title: first large text
    title = next((t for sz, t, _ in headings if sz == title_font), "Untitled Document")

    # Build outline
    outline = []
    for size, text, page in headings:
        if size == h1_font:
            level = "H1"
        elif size == h2_font:
            level = "H2"
        elif size == h3_font:
            level = "H3"
        else:
            continue
        outline.append({"level": level, "text": text, "page": page})

    return {"title": title, "outline": outline}

def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            data = extract_outline(pdf_path)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

