from fastapi import FastAPI,File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from Controller import AsyncCSVProcessor

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
    excel_file = await processor.process(file_bytes)

    return StreamingResponse(excel_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             headers={"Content-Disposition": "attachment; filename=result.xlsx"})
