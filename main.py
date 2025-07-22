#!/usr/bin/env python
# coding: utf-8

# In[6]:


import fitz  # PyMuPDF
import os
import json

# Your already working path
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

try:
    doc = fitz.open(pdf_path)
    print(f"Successfully opened: {pdf_path}")
except Exception as e:
    print("Error while opening PDF:", e)
    exit()

extracted_data = []

# Loop through each page
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text().strip()

    # Extract images
    images = []
    page_folder = os.path.join(output_dir, f"page_{page_num + 1}")
    os.makedirs(page_folder, exist_ok=True)

    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"image_{img_index + 1}.{image_ext}"
        image_path = os.path.join(page_folder, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        images.append(image_path)

    # Add to structured output
    extracted_data.append({
        "page": page_num + 1,
        "text": text,
        "images": images
    })

# Save JSON
json_path = os.path.join(output_dir, "extracted_content.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, indent=2, ensure_ascii=False)

print(" Extraction complete. JSON and images saved in:", output_dir)


# ## Imports:
# 
# ##### fitz is from the PyMuPDF library (used to read/extract PDF content)
# 
# #### os helps manage folders and file paths
# 
# ### json helps store output in a structured format
# 
# ## Setup paths:
# 
# #### pdf_path: your PDF file name
# 
# #### output_dir: folder where extracted content will be saved
# 
# #### os.makedirs(..., exist_ok=True) ensures the folder exists (creates it if not)
# 
# ## Open the PDF safely:
# 
# #### Tries to open the file
# 
# #### If it fails (e.g. file not found or corrupted), prints error and exits
# 
# ## For each page:
# 
# #### Loads the page
# 
# #### Extracts all text and removes extra whitespace with .strip()
# 
# #### Creates a subfolder for the current page like output/page_1/
# 
# #### Finds all images on the current page
# 
# #### Extracts each image using its internal reference (xref)
# 
# #### Saves the image as image_1.png, image_2.jpeg, etc.
# 
# #### Adds each image’s file path to a list for this page
# 
# #### Adds a dictionary with:
# 
# ###Page number
# 
# Text from that page
# 
# List of extracted image paths

# In[2]:


pip install pymupdf


# In[2]:


import fitz  # PyMuPDF
import os

# Step 1: File name
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
output_file = "extracted_text.txt"

# Step 2: Check if file exists
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f" File not found: {pdf_path}")
else:
    print(f"File found: {pdf_path}")

# Step 3: Open and extract
doc = fitz.open(pdf_path)
all_text = ""

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text()
    all_text += f"\n\n--- Page {page_num + 1} ---\n"
    all_text += text.strip()

# Step 4: Save to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"Text extraction complete. Saved to {output_file}")


# In[3]:


import fitz  # PyMuPDF
import os
import json

# Input PDF
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"

# Output folders
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Open the PDF
try:
    doc = fitz.open(pdf_path)
except Exception as e:
    print("Error while opening PDF:", e)
    exit()

# Store structured content
structured_content = []

# Loop through pages
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text().strip()

    # Prepare image saving
    page_folder = os.path.join(output_dir, f"page_{page_num + 1}")
    os.makedirs(page_folder, exist_ok=True)
    image_paths = []

    # Extract all images
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"image_{img_index + 1}.{image_ext}"
        image_path = os.path.join(page_folder, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        image_paths.append(image_path)

    # Append to structured list
    structured_content.append({
        "page": page_num + 1,
        "text": text,
        "images": image_paths
    })

# Write to JSON file
json_output_path = os.path.join(output_dir, "structured_output.json")
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(structured_content, json_file, indent=2, ensure_ascii=False)

print(f"Structured output saved to: {json_output_path}")


# In[ ]:




