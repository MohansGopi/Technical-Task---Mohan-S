# 📊 FastAPI CSV Analysis API

This project is a FastAPI-based service that allows users to upload a CSV file containing `Price`, `Volume`, and `time` columns. It calculates:
- rolling volume averages
- forward price returns
- binned ranges of both metrics
- a frequency matrix between volume and price movement.

The results are returned as:
- a downloadable Excel file (`.xlsx`)
- a JSON-formatted frequency table for frontend usage

---

## 📁 Project Structure

```
.
├── app/
│   ├── Server.py              # FastAPI app logic
│   ├── Controller.py          # Core logic for data processing
│   └── tmp/                   # Temporary folder for output Excel files
├── Frontend/                  # Frontend assets (e.g., index.html)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker setup for deployment
└── readme.md
```

---

## 🚀 Features

- ✅ Upload CSV files with market data
- 📈 Calculate rolling volume average and forward price return
- 🧮 Bin and categorize data into range intervals
- 📊 Create a frequency matrix of binned values
- 🧾 Download Excel file with raw and binned data
- 🔄 Serve frontend assets from `/Frontend`
- 🧹 Temporary file cleanup logic included

---

## 📦 Requirements

Install Python packages with:

```bash
pip install -r requirements.txt
```

Main dependencies:

- fastapi
- uvicorn
- pandas
- xlsxwriter
- python-multipart

---

## ▶️ Running the Server

From the project root:

```bash
cd app
uvicorn Server:app --reload
```

API docs will be available at:  
👉 `http://localhost:8000/docs`

---

## 🧪 API Endpoints

### 🔹 `POST /upload`

**Form Data:**
- `file` → CSV file (must include `Volume`, `Price`, `time`)
- `x` → Previous days for volume average
- `y` → Forward days for price return
- `i` → Bin size for volume % difference
- `j` → Bin size for price return %

**Returns:**
- JSON with:
  - Path to downloadable Excel file
  - Frequency table (`pandas.crosstab` output) in JSON format

---

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t csv-analyzer .
docker run -d -p 8000:8000 csv-analyzer
```
---

Visit:  
➡️ `http://localhost:8000/`

---
## 🧹 Temporary File Cleanup

The app uses a background task that runs every 60 minutes to delete Excel files older than 30 minutes from `app/tmp/`.

---

## 📄 License

This project was created for technical demonstration purposes. You may reuse or modify as needed.

---

## 🙋‍♂️ Author

**Mohan S**  
_Contributions welcome — feel free to fork or suggest improvements._