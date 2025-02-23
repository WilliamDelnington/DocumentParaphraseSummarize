import os, docx, fitz, io
def write_content_to_disk(file, file_path):
    if os.path.exists(file_path):
        return
    file.save(file_path)

    return file_path

def delete_content_from_disk(file_path):
    if not os.path.exists(file_path):
        return
    
    os.remove(file_path)

def read_file(file, filename: str):
    if filename.endswith('.txt'):
        text = file.read().decode('utf-8')

    elif filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(file.read()))
        text = "\n".join([p.text for p in doc.paragraphs])
    
    elif filename.endswith(".pdf"):
        file_stream = io.BytesIO(file.read())
        pdf = fitz.open(stream=file_stream, filetype="pdf")
        text = "\n".join([p.get_text() for p in pdf])

    else:
        raise ValueError("File is not supported")
    
    return text