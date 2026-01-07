import docx
import os

def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error reading file: {e}"

file_path = "AI Project Report Template .docx"
if os.path.exists(file_path):
    print(read_docx(file_path))
else:
    print(f"File not found: {file_path}")

