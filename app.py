import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import cv2
import easyocr
from pyzbar.pyzbar import decode
import os
import base64
import re
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

MONGO_URI = "mongodb+srv://vishwapanchal607:hack2024@cluster0.qatmn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "mydatabase"
COLLECTION_NAME = "mycollection"

def upload_data_to_mongodb(data):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_one(data)
        client.close()
    except Exception as e:
        st.error(f"Error uploading to MongoDB: {e}")

def save_to_pdf(data):
    pdf_filename = 'expiry_data.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, "Expiry Data Report")
    c.drawString(100, 730, f"Date of Purchase: {data[0]}")
    c.drawString(100, 710, f"Expiry Date: {data[1]}")
    c.drawString(100, 690, f"Item Name: {data[2]}")
    c.drawString(100, 670, f"Status: {data[3]}")
    c.save()
    return pdf_filename

def convert_expiry_date(expiry_string):
    patterns = [
        r'(\d{2})(\d{2})(\d{4})',
        r'(\d{2})(\d{2})(\d{2})'
    ]

    for pattern in patterns:
        match = re.search(pattern, expiry_string)
        if match:
            day, month, year = match.groups()
            if len(year) == 2:
                year = f'20{year}'
            return f"{day}-{month}-{year[-2:]}"
    return None

def extract_expiry_dates_from_image(image):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    extracted_text = " ".join([result[1] for result in results])
    expiry_dates = []
    for line in extracted_text.splitlines():
        for match in re.findall(r'\d{8}|\d{6}', line):
            result = convert_expiry_date(match)
            if result:
                expiry_dates.append(result)
    return expiry_dates

def extract_barcode_from_image(image):
    decoded_objects = decode(image)
    barcodes = [obj.data.decode('utf-8') for obj in decoded_objects]
    return barcodes

def lookup_product_name(barcode):
    response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json')
    if response.status_code == 200:
        product_data = response.json()
        if product_data.get("product"):
            return product_data["product"].get("product_name", "Product name not found")
        else:
            return "Product not found"
    return "API request failed"

def process_images(expiry_image, barcode_image):
    expiry_dates = extract_expiry_dates_from_image(expiry_image)
    barcode_names = {}

    if expiry_dates:
        for date in expiry_dates:
            print(f'Extracted Expiry Date: {date}')

    barcodes = extract_barcode_from_image(barcode_image)
    if barcodes:
        for barcode in barcodes:
            product_name = lookup_product_name(barcode)
            barcode_names[barcode] = product_name
            print(f'Extracted Barcode: {barcode}, Product Name: {product_name}')

    if expiry_dates and barcodes:
        return {
            "date_of_purchase": datetime.now().strftime('%d-%m-%y'),
            "expiry_date": expiry_dates[0],
            "item_name": barcode_names.get(barcodes[0], "Unknown Product"),
            "status": "Expired" if datetime.strptime(expiry_dates[0], "%d-%m-%y") < datetime.now() else "Valid"
        }
    return None

st.set_page_config(page_title="Food Safety Ration Tracker", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #1e1e1e;
            color: white;
            font-family: 'Helvetica', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #00adb5;
        }
        .stButton>button {
            background-color: #00adb5;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #393e46;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Food Safety Ration Tracker 🛡️")

expiry_images = []
barcode_images = []

st.write("Upload pairs of images (Expiry Date Image and Barcode Image).")

expiry_image_file = st.file_uploader("Upload Expiry Date Image (only jpg, jpeg, png)", type=["jpg", "jpeg", "png"], key="expiry_image", accept_multiple_files=False)
if expiry_image_file:
    expiry_image = cv2.imdecode(np.frombuffer(expiry_image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    expiry_images.append(expiry_image)

barcode_image_file = st.file_uploader("Upload Barcode Image (only jpg, jpeg, png)", type=["jpg", "jpeg", "png"], key="barcode_image", accept_multiple_files=False)
if barcode_image_file:
    barcode_image = cv2.imdecode(np.frombuffer(barcode_image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    barcode_images.append(barcode_image)

if st.button("Validate Ration") and len(expiry_images) >= 1 and len(barcode_images) >= 1:
    data = process_images(expiry_images[-1], barcode_images[-1])

    if data:
        pdf_filename = save_to_pdf(list(data.values()))
        upload_data_to_mongodb(data)
        st.success("Data successfully processed and uploaded to MongoDB!")

        st.write("### Extracted Data:")
        extracted_data_df = pd.DataFrame([data])
        st.dataframe(extracted_data_df)

        with open(pdf_filename, "rb") as pdf_file:
            b64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="expiry_data.pdf">Download PDF</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)
    else:
        st.error("No valid expiry dates or product names found.")

if st.button("Clear Images"):
    expiry_images.clear()
    barcode_images.clear()
    st.success("Uploaded images cleared.")
