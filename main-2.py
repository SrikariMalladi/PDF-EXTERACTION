#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pillow opencv-python


# In[3]:


import os
from PIL import Image
import cv2

# Input and output folders
input_folder = "output"     # Replace with actual image folder
output_folder = "output/processed_images"
os.makedirs(output_folder, exist_ok=True)

# Standard size for model input
TARGET_SIZE = (256, 256)

def preprocess_image(file_path, save_path):
    # Open image with Pillow
    image = Image.open(file_path).convert("RGB")

    # Convert to grayscale
    gray = image.convert("L")

    # Resize
    resized = gray.resize(TARGET_SIZE)

    # Optionally denoise (using OpenCV)
    opencv_img = cv2.cvtColor(np.array(resized), cv2.COLOR_GRAY2BGR)
    denoised = cv2.fastNlMeansDenoisingColored(opencv_img, None, 10, 10, 7, 21)

    # Save processed image
    final_img = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
    final_img.save(save_path)

# Loop through all images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        in_path = os.path.join(input_folder, filename)
        out_path = os.path.join(output_folder, filename)
        preprocess_image(in_path, out_path)

print("Preprocessing complete. Images saved to:", output_folder)


# In[4]:


pip install PyMuPDF


# In[5]:


import fitz  # PyMuPDF
import os

# Paths
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
output_folder = "output/raw_images"
os.makedirs(output_folder, exist_ok=True)

# Open the PDF
doc = fitz.open(pdf_path)
print(f"✅ Opened PDF: {pdf_path}")

image_count = 0

# Loop through each page
for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_filename = f"page{page_num + 1}_image{img_index + 1}.{image_ext}"
        image_path = os.path.join(output_folder, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_count += 1
        print(f"🔹 Extracted {image_filename}")

doc.close()
print(f"\n Done! Extracted {image_count} images into: {output_folder}")


# In[6]:


pip install transformers torch torchvision


# In[1]:


import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-vqa-base")

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Folders
input_folder = "output"
output_json = "output/generated_questions.json"

# Store results
results = []

# Loop through each image
for filename in sorted(os.listdir(input_folder)):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGB")

        # Prompt to BLIP
        prompt = "What question does this image represent?"

        inputs = processor(image, prompt, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        generated_question = processor.decode(out[0], skip_special_tokens=True)

        results.append({
            "image": image_path,
            "generated_question": generated_question
        })

        print(f"{filename} → {generated_question}")

# Save to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\n All questions saved to: {output_json}")


# In[ ]:




