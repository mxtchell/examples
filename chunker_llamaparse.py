
import json
import os
import pandas as pd
import base64
# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
# Initialize the parser with your API key
parser = LlamaParse(
  api_key="xx",
  use_vendor_multimodal_model=True,
  vendor_multimodal_model_name="openai-gpt4o",
  vendor_multimodal_api_key="xx",
  result_type="markdown",
  page_prefix="START OF PAGE: {pageNumber}\n",
  page_suffix="\nEND OF PAGE: {pageNumber}"
)
# Define the path for the PDF file and output JSON file
pdf_path = 'x'
output_json_path = 'x'
# Initialize an empty list to hold the documents with metadata
pdf_texts = []
# Function to read a PDF file and convert it to a base64 string
def pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        encoded_bytes = base64.b64encode(pdf_file.read())
    return encoded_bytes
# Convert the PDF to base64
pdf_base64 = pdf_to_base64(pdf_path)
# Parse the PDF file using the base64 representation
documents = parser.load_data(open(pdf_path, "rb"), extra_info={"file_name": os.path.basename(pdf_path)})
# Initialize a dictionary to hold the PDF's metadata and chunks
pdf_dict = {
    "File": os.path.basename(pdf_path),
    "Description": "to fill in",
    "Summary": "to fill in",
    "Chunks": []
}
page = 0
chunk_num = 0
for document in documents:
    page_text = document.text
    if "START OF PAGE:" in page_text:
        start_index = page_text.find("START OF PAGE:") + len("START OF PAGE:")
        end_index = page_text.find("\n", start_index)
        if end_index != -1:
            try:
                page = int(page_text[start_index:end_index].strip())
            except ValueError:
                pass  # Keep the current page number if extraction fails
    pdf_dict["Chunks"].append({
        "Chunk": chunk_num,
        "Text": document.text,
        "Page": page,
    })
    chunk_num += 1
pdf_texts.append(pdf_dict)
# Save the documents with metadata into a JSON file in the same directory as the PDF
with open(output_json_path, 'w') as outfile:
    json.dump(pdf_texts, outfile, indent=4)
print(f"Documents with metadata saved to {output_json_path}")