import fitz  # PyMuPDF
import re

def parse_metraj_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    metraj_list = []

    for page in doc:
        text = page.get_text()

        # Basit desenler - ileride daha güçlü eşleştirme yapılacak
        matches = re.findall(r"Ø(\d+).*?L:(\d+)[^\d]+([\d,.]+)[^\d]+([\d,.]+)", text)
        for match in matches:
            cap, uzunluk, akar1, akar2 = match
            metraj_list.append({
                "boru_cap": int(cap),
                "uzunluk_m": int(uzunluk),
                "akar_kotu_1": akar1.replace(",", "."),
                "akar_kotu_2": akar2.replace(",", ".")
            })

    return metraj_list
