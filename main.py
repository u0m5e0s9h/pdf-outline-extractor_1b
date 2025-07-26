import os
import json
import fitz  
from datetime import datetime
from collections import defaultdict


def extract_text_with_headings(pdf_path):
    """
    Extract headings and text from the PDF.
    We treat larger/bolder fonts as headings, others as normal text.
    Returns a list of sections with page number.
    """
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue

                
                font_sizes = [span["size"] for span in line["spans"]]
                max_font = max(font_sizes)

                
                if max_font > 15:
                    level = "H1"
                elif 12 < max_font <= 15:
                    level = "H2"
                else:
                    level = "H3"

                sections.append({
                    "text": text,
                    "page": page_num,
                    "level": level
                })
    return sections

def keyword_score(text, keywords):
    """Simple scoring function based on keyword matches."""
    score = 0
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 1
    return score

def rank_sections(all_sections, job_description):
    """
    Rank sections based on relevance to the job description.
    For now, use simple keyword overlap.
    """
    keywords = job_description.split()  
    scored_sections = []
    for sec in all_sections:
        score = keyword_score(sec["text"], keywords)
        if score > 0:
            scored_sections.append((score, sec))

    
    scored_sections.sort(key=lambda x: x[0], reverse=True)
    
    ranked = []
    for i, (_, sec) in enumerate(scored_sections, start=1):
        ranked.append({
            "document": sec["document"],
            "section_title": sec["text"],
            "importance_rank": i,
            "page_number": sec["page"]
        })
    return ranked

def summarize_section(text, max_sentences=2):
    """
    Naive summary: take first N sentences.
    """
    sentences = text.split(". ")
    return ". ".join(sentences[:max_sentences]) + ('.' if sentences else '')


def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    persona_path = os.path.join(input_dir, "persona.txt")
    job_path = os.path.join(input_dir, "job.txt")

    persona = open(persona_path, "r", encoding="utf-8").read().strip()
    job_to_be_done = open(job_path, "r", encoding="utf-8").read().strip()


    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    all_sections = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        sections = extract_text_with_headings(pdf_path)
        for sec in sections:
            sec["document"] = pdf_file
        all_sections.extend(sections)

    
    ranked_sections = rank_sections(all_sections, job_to_be_done)

    
    subsection_analysis = []
    for sec in ranked_sections[:5]:  
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": summarize_section(sec["section_title"]),
            "page_number": sec["page_number"]
        })

    # Prepare output JSON
    output_data = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": ranked_sections,
        "subsection_analysis": subsection_analysis
    }

    # Write output.json
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "output.json"), "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print("Processing completed. Output saved to output.json")

if __name__ == "__main__":
    main()
