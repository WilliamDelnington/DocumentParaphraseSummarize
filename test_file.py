# import readfile
import re
import json

# reader = readfile.ReadFile("./testDocument.txt")
# text = reader.read()

# print(text)
with open("./responses.json") as j:
  dataset = json.loads(j.read())

for data in dataset:
  if data["intent"]["tags"] == "greeting":
    print(data["intent"]["patterns"][2])
    patterns = data["intent"]["patterns"][2]

    texts = [
        "how are you",
        "How are you",
        "How Are You?",
        "how are you?",
        "How are you?"
    ]

    for text in texts:
      if (re.search(patterns, text)):
          print(f"Match found in: '{text}'")
      else:
          print(f"No match found in: '{text}'")



# string = "This document contains 300 words and the other document contains 250 words"
# pattern = r"\d+\swords"

# print(re.search(pattern, string).group())