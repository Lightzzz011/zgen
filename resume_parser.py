import spacy
import PyPDF2

# Load small English model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Extract top keywords from text
def extract_keywords(text, top_n=20):
    doc = nlp(text.lower())
    keywords = [token.text for token in doc if token.pos_ in ["NOUN","PROPN"]]
    freq = {}
    for k in keywords:
        freq[k] = freq.get(k,0)+1
    top_keywords = sorted(freq, key=freq.get, reverse=True)[:top_n]
    return top_keywords
