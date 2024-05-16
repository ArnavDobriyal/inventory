import pytesseract
from PIL import Image
from docx import Document

# Load the image
image_path = "C:\\Users\\dobri\\OneDrive\\Pictures\\WhatsApp Image 2024-05-14 at 19.48.57.jpeg"
img = Image.open(image_path)

# Perform OCR to extract text from the image
extracted_text = pytesseract.image_to_string(img)

# Create a new Word document
doc = Document()

# Add the extracted text to the Word document
doc.add_paragraph(extracted_text)

# Save the Word document
doc.save('extracted_text.docx')
