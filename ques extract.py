#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-vqa-base")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Paths
input_folder = "output"
output_json = "output/grouped_questions.json"

# Get all image files sorted
image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg'))])

# Group into chunks: [Q, Option1, Option2, Option3]
grouped = [image_files[i:i + 4] for i in range(0, len(image_files), 4)]

results = []

for group in grouped:
    if len(group) < 4:
        continue  # skip incomplete groups

    question_image = os.path.join(input_folder, group[0])
    option_images = [os.path.join(input_folder, f) for f in group[1:]]

    # Generate question with BLIP
    image = Image.open(question_image).convert("RGB")
    prompt = "What question does this image represent?"
    inputs = processor(image, prompt, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    generated_question = processor.decode(out[0], skip_special_tokens=True)

    results.append({
        "question": generated_question,
        "question_image": question_image,
        "option_images": option_images,
        "answer": None  # Optional: You can fill this manually
    })

    print(f" Generated question for {group[0]}: {generated_question}")

# Save final structured JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\n All grouped questions saved to: {output_json}")


# In[ ]:




