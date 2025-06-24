import io
import re
import fitz
import docx
import pytesseract
import pdfplumber
from PIL import Image
from keybert import KeyBERT
from transformers import pipeline

kw_model = KeyBERT()
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# ──────── 1. Extract Title & Author from PDF Layout ─────────
def extract_title_author_from_pdf_bytes(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        first = pdf.pages[0]
        words = first.extract_words(extra_attrs=["size", "top"])
        lines_map = {}
        for w in words:
            y = round(w["top"])
            lines_map.setdefault(y, []).append(w["text"])
        header_lines = [" ".join(lines_map[y]).strip() for y in sorted(lines_map.keys())]

        title = header_lines[0] if header_lines else "Not found"
        author = "Not found"
        for line in header_lines[1:4]:
            if re.search(r"[A-Za-z]", line):
                author = line
                break
        return title.strip().title(), author.strip().title()

# ──────── 1B. Fallback Title/Author from Text ─────────
def extract_author_from_text(text):
    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if 3 < len(line.strip()) < 100]

    # 1. Look for lines starting with "Dr.", "Prof.", etc.
    for line in lines[:15]:
        if re.match(r"^(Dr\.|Prof\.|Mr\.|Ms\.)", line):
            return line.strip().title()

    # 2. Look for a capitalized line with 2–4 words (likely a name)
    for line in lines[:10]:
        if line.count(" ") in [1, 2, 3] and line[0].isupper():
            if all(w[0].isupper() for w in line.split() if w.isalpha()):
                return line.strip().title()

    return "Not found"


# ──────── 2. Extract Text from Various Formats ─────────
def extract_text_from_pdf(file):
    content = file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text
        else:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img)
    return text, content

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text(file, filetype):
    if filetype == "pdf":
        text, content = extract_text_from_pdf(file)
        return text, content
    elif filetype == "docx":
        return extract_text_from_docx(file), None
    elif filetype == "txt":
        data = file.read().decode("utf-8", errors="ignore")
        return data, None
    else:
        return "", None

# ──────── 3. Clean Text ─────────
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# ──────── 4. Extract Keywords ─────────
def extract_keywords(text, num=5):
    return [kw[0] for kw in kw_model.extract_keywords(text[:1000], top_n=num)]

# ──────── 5. Extract Summary ─────────
def extract_summary(text):
    text = text.replace('\n', ' ')
    paras = re.split(r'\.\s+', text)
    start = '. '.join(paras[:5])

    if len(start) < 300:
        return "Text too short to summarize."

    try:
        summ = summarizer(start, max_length=120, min_length=40, do_sample=False)[0]['summary_text']
        return summ.strip().replace("This article", "This document")
    except Exception as e:
        return "Summary not available (" + str(e) + ")"

# ──────── 6. Extract Date ─────────
def extract_date(text):
    # Format: November 12, 2024
    match1 = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}", text, re.IGNORECASE)
    if match1:
        return match1.group(0)

    # Format: 12 November 2024
    match2 = re.search(r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}", text, re.IGNORECASE)
    if match2:
        return match2.group(0)

    # Format: 12/11/2024 or 12-11-2024
    match3 = re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    if match3:
        return match3.group(0)

    return "Not found"

# ──────── 7. Map Topics ─────────
def map_to_topics(keywords):
    topics = {
        "Finance": ["loan","investment","stock","bank","equity","inflation","interest","capital","debt","credit"],
        "Health": ["virus","vaccine","health","disease","hospital","doctor","mental","therapy","epidemic","covid"],
        "Education": ["school","student","exam","university","curriculum","teaching","learning","faculty","class"],
        "Environment": ["climate","pollution","carbon","green","energy","sustainability","biodiversity","conservation"],
        "Technology": ["ai","data","machine","model","cloud","blockchain","algorithm","robotics","digital","software"],
        "Governance": ["policy","government","planning","development","infrastructure","scheme","bureaucracy","district"],
        "Society": ["gender","inequality","poverty","caste","culture","democracy","justice","migration","tribal"],
        "Agriculture": ["crop","irrigation","farmer","yield","harvest","fertilizer","pesticide","rural"]
    }
    found = {t for t, kwlist in topics.items() for kw in keywords for w in kwlist if kw in w.lower()}
    return list(found) if found else ["Uncategorized"]

# ──────── 8. Master Metadata Extractor ─────────
def extract_metadata(file, filetype):
    raw_text, pdf_bytes = extract_text(file, filetype)
    cleaned = clean_text(raw_text)

    if filetype == "pdf" and pdf_bytes:
        title, author = extract_title_author_from_pdf_bytes(pdf_bytes)
    else:
        # Basic fallback for title
        title = cleaned.split('.')[0][:120].strip().title() if '.' in cleaned else "Not found"
        author = extract_author_from_text(cleaned)

    return {
        "title": title,
        "author": author,
        "date": extract_date(cleaned),
        "keywords": extract_keywords(cleaned),
        "topics": map_to_topics(extract_keywords(cleaned)),
        "summary": extract_summary(cleaned),
        "preview": cleaned[:3000]
    }
