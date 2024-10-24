# Food Safety Ration Tracker 🛡️

The **Food Safety Ration Tracker** is a web application designed to help users manage food safety by tracking expiry dates and product information using image recognition. The app leverages Optical Character Recognition (OCR) to extract expiry dates from images and barcodes from product packaging, integrating this data into a MongoDB database and allowing users to download a detailed PDF report.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Image Uploads**: Users can upload images of expiry dates and barcodes.
- **Data Extraction**: The app uses OCR to extract expiry dates and product names from images.
- **MongoDB Integration**: Extracted data is stored in a MongoDB database for persistent storage.
- **PDF Reports**: Users can download a PDF report containing extracted data.
- **User-Friendly Interface**: Designed using Streamlit for an intuitive experience.

## Technologies

- **Python**: The programming language used for backend logic.
- **Streamlit**: Framework for building web applications.
- **OpenCV**: Library for image processing.
- **EasyOCR**: Library for optical character recognition.
- **PyZbar**: Library for barcode decoding.
- **MongoDB**: NoSQL database for data storage.
- **ReportLab**: Library for generating PDF files.
- **Requests**: Library for making HTTP requests to external APIs.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/<your-username>/food-safety-ration-tracker.git
    cd food-safety-ration-tracker
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB**: 
   - Create a MongoDB Atlas account or install MongoDB locally.
   - Create a new database and collection.
   - Update the `MONGO_URI` in the code with your MongoDB connection string.

## Usage

1. **Run the application**:
    ```bash
    streamlit run app.py
    ```

2. **Upload images**:
   - Use the file uploaders to upload the expiry date image and barcode image.
   
3. **Validate Ration**:
   - Click the "Validate Ration" button to process the images. The extracted data will be displayed, and you will have the option to download a PDF report.

4. **Clear Images**:
   - Click the "Clear Images" button to reset the uploaded images.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

