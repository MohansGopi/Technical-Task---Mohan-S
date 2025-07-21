from fastapi import FastAPI,File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from Controller import AsyncCSVProcessor
import datetime
app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    i: float = Form(...),
    j: float = Form(...)
):
    file_bytes = await file.read()
    processor = AsyncCSVProcessor(x, y, i, j)
    excel_file,frequecyTable = await processor.process(file_bytes)
    temp_excel_path = f"./tmp/result{datetime.datetime.now()}.xlsx"
    with open(temp_excel_path, "wb") as f:
        f.write(excel_file.getvalue())

    return {
        "Table":frequecyTable.to_dict(orient="split"),
        "XlPath":temp_excel_path
    }
