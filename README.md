# PDF Outline Extractor

This project extracts a structured outline from PDF files, including the **document title** and **headings (H1, H2, H3)** with their page numbers.
The output is a valid JSON file following the required schema.

---

## **Approach**

1. **PDF Parsing:**
   We use the `PyMuPDF` library to read the PDF and extract text and metadata.

2. **Heading Detection:**

   * We analyze text attributes (font size, boldness, position) to differentiate between Title, H1, H2, and H3.
   * Heuristics are applied to handle PDFs that don’t strictly follow font-size conventions.

3. **JSON Output:**
   For each PDF, a JSON file is generated in `/app/output` with the following structure:

   ```json
   {
     "title": "Understanding AI",
     "outline": [
       { "level": "H1", "text": "Introduction", "page": 1 },
       { "level": "H2", "text": "What is AI?", "page": 2 },
       { "level": "H3", "text": "History of AI", "page": 3 }
     ]
   }
   ```

---

## **Libraries Used**

* **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/):**
  Used for PDF text extraction, font analysis, and page navigation.

* **`json` (Python standard library):**
  For building and writing structured JSON output.

* **`os` (Python standard library):**
  For scanning input/output directories.

---

## **Build and Run Instructions**

> **Note:** Your solution will work offline as per the hackathon requirements.

### **1. Build the Docker Image**

In the project root directory (where `Dockerfile` is located):

```bash
docker build --platform=linux/amd64 -t pdf-outline-extractor .
```

---

### **2. Run the Container**

Prepare the `input/` and `output/` directories:

```
project-root/
 ├── input/   (place your PDF files here)
 ├── output/  (JSON files will be generated here)
```

Run:

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor
```

---

### **3. Output**

For every `filename.pdf` in `/app/input`, a corresponding `filename.json` will be created in `/app/output`.

---

## **Expected Execution**

Your container will automatically:

1. Process **all PDFs** from `/app/input`.
2. Generate valid JSON files in `/app/output`.
