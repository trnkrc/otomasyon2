import fitz  # PyMuPDF

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
                        w = span['text'].strip()
                        if w:
                            words.append(w)

        i = 0
        while i < len(words):
            if words[i].startswith("Ø") or words[i] == "Ø":
                try:
                    if words[i].startswith("Ø") and len(words[i]) > 1:
                        cap = int(words[i][1:])
                    else:
                        cap = int(words[i+1] + words[i+2])
                        i += 2

                    if words[i+1] == "L" or words[i+1] == "L:":
                        uzunluk = int(words[i+2])
                        i += 2
                    elif words[i+1].startswith("L:"):
                        uzunluk = int(words[i+1].split(":")[1])
                    else:
                        uzunluk = int(words[i+1])

                    akar1 = _combine_number(words[i+2:i+5])
                    akar2 = _combine_number(words[i+5:i+8])

                    metraj_list.append({
                        "boru_cap": cap,
                        "uzunluk_m": uzunluk,
                        "akar_kotu_1": akar1,
                        "akar_kotu_2": akar2
                    })
                    i += 8
                except:
                    i += 1
            else:
                i += 1

    return metraj_list

def _combine_number(pieces):
    digits = [p for p in pieces if p.replace(",", ".").replace(".", "").isdigit() or p in [".", ","]]
    number = "".join(digits).replace(",", ".")
    return number
