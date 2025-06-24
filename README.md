# 📄 DocuTag — Automated Metadata Extraction from Documents

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
- Uses KeyBERT for keyword extraction and Hugging Face transformers for summarization
- Supports scanned PDFs with OCR (via pytesseract)
- Clean and responsive web UI built with Streamlit
- Ready for deployment on Streamlit Cloud

---

## Folder Structure

docutag/
├── app.py # Streamlit app 
├── utils.py # Core backend logic and NLP functions
├── requirements.txt # Dependencies for setup
├── README.md 
└── sample_files/ # Sample documents to test


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
## Demo Video

🔗 [Watch the demo](https://drive.google.com/drive/folders/1EK_NSyOi0oe5Jb9Fj79YZb1809r5AiJF?usp=sharing)

---