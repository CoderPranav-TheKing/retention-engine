import os
import random
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def upload_page():
    return """
    <html>
        <body>
            <h2>Upload Sales CSV</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file" required>
                <input type="submit">
            </form>
        </body>
    </html>
    """


def generate_message(name, items, discount, coupon):
    prompt = f"""
    Write a warm, friendly WhatsApp thank-you message.

    Customer Name: {name}
    Items Purchased: {items}
    Offer: {discount}
    Coupon Code: {coupon}

    Keep it under 60 words.
    Make it feel personal and premium.
    """

    response = model.generate_content(prompt)
    return response.text.strip()


@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    required_columns = {"name", "phone", "items", "amount", "date"}
    if not required_columns.issubset(set(df.columns)):
        return HTMLResponse(
            """
            <h3>❌ Invalid CSV Format</h3>
            <p>Required columns: name, phone, items, amount, date</p>
            <a href="/">Go Back</a>
        """
        )

    results_html = ""
    processed_count = 0

    for _, row in df.iterrows():
        name = row["name"]
        phone = str(row["phone"])
        items = row["items"]
        amount = float(row["amount"])

        # Simple discount logic
        if amount > 2000:
            discount = "15% OFF"
        elif amount > 1000:
            discount = "10% OFF"
        else:
            discount = "5% OFF"

        coupon_code = f"LOYAL{random.randint(1000,9999)}"

        # Generate AI message
        message = generate_message(name, items, discount, coupon_code)

        # Log to terminal
        print("------")
        print(f"Customer: {name} | Phone: {phone}")
        print(message)
        print("------")

        # Add to HTML output
        results_html += f"""
        <div style="border:1px solid #ccc;padding:10px;margin:10px;">
            <b>{name}</b> ({phone})<br>
            <b>Offer:</b> {discount}<br>
            <b>Coupon:</b> {coupon_code}<br><br>
            <b>Generated Message:</b><br>
            {message}
        </div>
        """

        processed_count += 1

    return f"""
    <html>
        <body>
            <h2>Upload Successful ✅</h2>
            <p>Processed {processed_count} customers.</p>
            {results_html}
            <br><br>
            <a href="/">Upload Another File</a>
        </body>
    </html>
    """
