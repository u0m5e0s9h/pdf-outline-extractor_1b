# Approach Explanation

## 1. Problem Understanding

The challenge is to build an intelligent document analysis system that processes multiple PDF documents (3–10 files) along with a given **persona** and a **job-to-be-done**. The system must extract and prioritize the most relevant sections from the documents and produce a structured **JSON output**. The output contains metadata, a ranked list of important sections, and refined sub-sections related to the persona’s goal.

The core idea is to simulate how a human analyst would quickly identify and extract key content tailored to a specific purpose (e.g., a researcher preparing a literature review or an analyst summarizing financial reports).

---

## 2. Methodology

### 2.1 Input Handling

The system reads:

* **PDF files** from the `/app/input` directory.
* A `persona.txt` file describing the user’s role and expertise.
* A `job.txt` file defining the task that needs to be completed.

The filenames of the PDFs are stored as part of the metadata in the final output.

---

### 2.2 Text Extraction

We use **PyMuPDF (`fitz`)** for PDF parsing. It enables:

* Extraction of text along with layout information such as page numbers.
* Identification of section headings using font size, style, or keyword-based heuristics.
  This ensures that even complex documents with mixed formatting can be processed.

---

### 2.3 Relevance Scoring and Ranking

To determine which sections are most relevant:

1. The system tokenizes the extracted text into **sections or headings**.
2. It evaluates each section’s similarity to the `persona` and `job-to-be-done`.

   * A simple **TF-IDF (Term Frequency–Inverse Document Frequency)** approach is used to measure keyword overlap between the section and the job description.
   * Sections are ranked by a relevance score.
3. The top-ranked sections are assigned **importance\_rank** values in the final JSON.

---

### 2.4 Subsection Analysis

For each highly ranked section, the text is further refined by:

* Extracting **bullet points, numbered lists, or paragraph summaries**.
* Removing redundant or unrelated content.

This results in concise, actionable content tailored to the persona’s needs.

---

### 2.5 Output JSON

The final JSON has three main components:

* **Metadata:** Input documents, persona, job, and processing timestamp.
* **Extracted Sections:** A ranked list of key sections with page numbers.
* **Subsection Analysis:** Refined content from the important sections.

---

## 3. Libraries and Tools

* **PyMuPDF (`fitz`)** – PDF text and layout extraction.
* **NLTK/Scikit-learn** – TF-IDF scoring and keyword matching.
* **Python Standard Library** – For JSON handling, timestamps, and directory management.

---

## 4. Performance and Constraints

* The solution is designed to run on **CPU-only environments** with no internet access.
* Processing time for 3–5 documents (up to 50 pages each) is well within **60 seconds**.
* No external APIs or large models (>1 GB) are used, keeping the solution lightweight and self-contained.

---

## 5. Key Challenges and Design Choices

* **Heading Detection:** Font-size-based heuristics combined with keyword analysis (e.g., "Introduction", "Summary").
* **Relevance Ranking:** Balancing simple keyword overlap with semantic meaning.
* **Offline Execution:** The entire solution works without online dependencies.
