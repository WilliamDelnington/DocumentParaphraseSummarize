import pypdf

file = pypdf.PdfReader("./OOP_2013.pdf")
print(file.pages[0].extract_text())