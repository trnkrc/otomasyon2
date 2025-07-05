# pdfmetraj-api/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf_utils import parse_metraj_pdf

app = FastAPI()

@app.post("/extract-metraj")
async def extract_metraj(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Yalnizca PDF dosyalari kabul edilir."}, status_code=400)

    contents = await file.read()
    try:
        results = parse_metraj_pdf(contents)
        return {"data": results}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# pdfmetraj-api/pdf_utils.py
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
                    # Ø400 olabilir ya da Ø + 400 ayrı olabilir
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

                    # Akar kotlarını dene
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
    """88 . 54 -> 88.54 gibi sayıları birleştir."""
    digits = [p for p in pieces if p.replace(",", ".").replace(".", "").isdigit() or p in [".", ","]]
    number = "".join(digits).replace(",", ".")
    return number

# pdfmetraj-api/requirements.txt
fastapi
uvicorn
PyMuPDF
python-multipart

# pdfmetraj-api/README.md
# PDF Metraj API

Bu servis, altyapi projelerine ait PDF dosyalarindan otomatik metraj verisi cikarir.

## Kurulum
```
pip install -r requirements.txt
```

## Calistirma
```
uvicorn main:app --reload
```

## API
**POST /extract-metraj**  
PDF dosyasini gonderin, JSON metraj verisi alin.

---

Bu surumde parcalanmis PDF yapi metinlerini sirali olarak gezip Ø, L, ve akar kotlarini yakalamaya calisir. Nokta ve sayilarin bolunmus oldugu durumlara toleranslidir.
