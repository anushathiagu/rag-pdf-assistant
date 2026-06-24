import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def get_answer(text_chunks, question):
    model = genai.GenerativeModel("gemini-2.0-flash")
    context = "\n\n".join(text_chunks[:5])
    prompt = f"Answer based on this context:\n{context}\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text