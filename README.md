# DocuTag — Automated Metadata Extraction from Documents

DocuTag is a smart web application that automatically extracts meaningful metadata from unstructured documents such as PDFs, DOCX, and TXT files. It uses modern NLP techniques, OCR support, and keyword/topic analysis to generate structured metadata like **Title, Author, Date, Keywords, Topics**, and a concise **Summary**.

---

## Features

- Upload documents in `.pdf`, `.docx`, or `.txt` format
- Extracts:
  - Title
  - Author(s)
  - Date
  - Top Keywords
  - Topic Category
  - Summary
  - Full text preview
- Uses KeyBERT for keyword extraction and Hugging   Face transformers for summarization
- Supports scanned PDFs with OCR (via pytesseract)
- Clean and responsive web UI built with Streamlit
- Ready for deployment on Streamlit Cloud

---

## Folder Structure

docutag/
├── app.py # Streamlit web application
├── utils.py # Core backend logic (text + metadata extraction)
├── docutag_demo.ipynb # Jupyter notebook demo of full backend logic
├── requirements.txt # Python dependencies
├── README.md # Project overview and setup guide
└── sample_files/ # (Optional) Test documents


---

## Installation

1. **Clone the repository:**


git clone https://github.com/yashasvipandey26/docutag.git
cd docutag

2. **Install dependencies:**

pip install -r requirements.txt

3. **Run the app:**

streamlit run app.py


---

## Jupyter Notebook Demo

If you want to test the metadata extraction logic without running the Streamlit app, you can use the notebook:

> Open [`docutag_demo.ipynb`](docutag_demo.ipynb)  
> Upload a file and run the cells to view metadata extraction results.

---

## Demo Video

🔗 [Watch the demo](https://drive.google.com/drive/folders/1EK_NSyOi0oe5Jb9Fj79YZb1809r5AiJF?usp=sharing)

---

## Tech Stack

- **Streamlit** — for frontend UI
- **Python** — core logic
- **KeyBERT** — keyword extraction
- **Transformers (Hugging Face)** — text summarization
- **spaCy** — Named Entity Recognition (optional)
- **PyMuPDF + pdfplumber** — PDF text layout analysis
- **pytesseract + Pillow** — OCR for scanned documents

---