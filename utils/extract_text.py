from pdfminer.high_level import extract_text as extract_pdf_text
import PyPDF2
from utils.classify_links import classify_links_with_llm


def extact_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        text = extract_pdf_text(file)
    return text
    
    
def extract_links(file):
    links = []
    PDF = PyPDF2.PdfReader(file)
    pages = len(PDF.pages) 
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    for page_num in range(pages):
        pageObject = PDF.pages[page_num] 
        if key in pageObject: 
            ann = pageObject[key]
            for a in ann:
                u = a.get_object() 
                if ank in u and uri in u[ank]:
                    links.append(u[ank][uri])

    extracted_links = classify_links_with_llm(links)
    return extracted_links
    
    
def extract_text_and_links(file):
    extracted_text = extact_text(file)
    extracted_links = extract_links(file)
    
    return extracted_text, extracted_links