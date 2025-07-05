import fitz  # PyMuPDF
import re

def parse_metraj_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    metraj_list = []

    for page in doc:
        blocks = page.get_text("dict")['blocks']
        words = []
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        words.append({
                            "text": span['text'],
                            "x": span['bbox'][0],
                            "y": span['bbox'][1]
                        })

        # Kelimeleri Y eksenine göre grupla
        rows = {}
        for w in words:
            y_key = round(w['y'], 1)
            rows.setdefault(y_key, []).append(w)

        for y, items in rows.items():
            sorted_items = sorted(items, key=lambda x: x['x'])
            line_text = " ".join([w['text'] for w in sorted_items])
            match = re.search(r"Ø\s?(\d{3}).*?L\s?:?\s?(\d+).*?([\d,.]+).*?([\d,.]+)", line_text)
            if match:
                cap, uzunluk, akar1, akar2 = match.groups()
                metraj_list.append({
                    "boru_cap": int(cap),
                    "uzunluk_m": int(uzunluk),
                    "akar_kotu_1": akar1.replace(",", "."),
                    "akar_kotu_2": akar2.replace(",", ".")
                })

    return metraj_list
