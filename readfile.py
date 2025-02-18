from docx import Document
import win32com.client
import pdfplumber

class ReadFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filetype = self.filepath.split(".")[-1]

    def read(self):
        if self.filetype == "txt":
            self.readTxt()

        elif self.filetype == "doc":
            self.readDoc()

        elif self.filetype == "docx":
            self.readDocx()

        elif self.filetype == "pdf":
            self.readPdf()

        return self.text if self.text else None

    def readDocx(self):
        doc = Document(self.filepath)
        self.text = ""

        for para in doc.paragraphs:
            self.text += para + "\n"

    def readDoc(self):
        self.text = ""
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(self.filepath)
        self.text = doc.Content.Text

    def readPdf(self):
        self.text = ""
        with pdfplumber.open(self.filepath) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text()

    def readTxt(self):
        self.text = ""
        with open(self.filepath, "r", encoding="utf-8") as file:
            self.text = file.read()