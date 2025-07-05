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
