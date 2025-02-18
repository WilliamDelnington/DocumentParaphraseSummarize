import readfile

reader = readfile.ReadFile("./testDocument.txt")
text = reader.read()

print(text)