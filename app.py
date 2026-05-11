from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import subprocess, os, uuid, base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    if not file.filename.endswith(".epub"):
        return {"error": "শুধু EPUB ফাইল দাও"}

    job_id = str(uuid.uuid4())
    input_path  = f"/tmp/{job_id}.epub"
    output_path = f"/tmp/{job_id}.azw3"

    content = await file.read()
    with open(input_path, "wb") as f:
        f.write(content)

    try:
        result = subprocess.run(
            ["ebook-convert", input_path, output_path],
            capture_output=True,
            timeout=180
        )
    except subprocess.TimeoutExpired:
        return {"error": "Timeout — ফাইলটা অনেক বড়"}

    if result.returncode != 0:
        return {"error": "Conversion failed"}

    with open(output_path, "rb") as f:
        data = f.read()

    os.remove(input_path)
    os.remove(output_path)

    return {
        "filename": file.filename.replace(".epub", ".azw3"),
        "data": base64.b64encode(data).decode()
    }
