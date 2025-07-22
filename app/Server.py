from fastapi import FastAPI,File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from Controller import AsyncCSVProcessor
from datetime import timedelta, datetime
import os
import asyncio


app = FastAPI()

TEMP_DIR = "./tmp"
FILE_LIFETIME = timedelta(hours=0.5)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

async def delete_old_temp_files():
    while True:
        now = datetime.now()
        print("🧹 Cleaning up old temp files...")

        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            try:
                file_stat = os.stat(file_path)
                file_age = now - datetime.fromtimestamp(file_stat.st_mtime)

                if file_age > FILE_LIFETIME:
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")
            except Exception as e:
                print(f"⚠️ Error deleting {file_path}: {e}")

        await asyncio.sleep(3600)  # wait 1 hour before next check

@app.on_event("startup")
async def start_cleanup_task():
    asyncio.create_task(delete_old_temp_files())


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
    temp_excel_path = f"./tmp/result{datetime.now()}.xlsx"
    with open(temp_excel_path, "wb") as f:
        f.write(excel_file.getvalue())

    return {
        "Table":frequecyTable.to_dict(orient="split"),
        "XlPath":temp_excel_path
    }

@app.get("/download/{filepath}")
async def downloadFile(filepath:str):
    path = f"./tmp/{filepath}"
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename=filepath)