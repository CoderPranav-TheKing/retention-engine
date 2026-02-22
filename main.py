from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()


# Simple Upload Page
@app.get("/", response_class=HTMLResponse)
def upload_page():
    return """
    <html>
        <body>
            <h2>Upload Sales CSV</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """


# Handle CSV Upload
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    for index, row in df.iterrows():
        print(row)

    return {"status": "File processed successfully"}


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port)
