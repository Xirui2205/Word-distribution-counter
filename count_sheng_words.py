import json
import re
from collections import Counter
from pathlib import Path
import csv

# path to your JSON export
IN_FILE = Path("data/annotations.json")
OUT_FILE = Path("sheng_word_distribution.csv")

# simple regex tokenizer (keeps a-z letters)
TOKEN_RE = re.compile(r"[a-zA-Z’']+")

def extract_sheng_text(data):
    """Return list of all Sheng sentences from Label Studio JSON"""
    sheng_sentences = []
    for task in data:
        for ann in task.get("annotations", []):
            for result in ann.get("result", []):
                if result.get("from_name") == "sheng":
                    text = result["value"]["text"][0]
                    sheng_sentences.append(text)
    return sheng_sentences

def tokenize(sentence):
    return [t.lower() for t in TOKEN_RE.findall(sentence)]

def main():
    with open(IN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]

    sheng_sentences = extract_sheng_text(data)

    tokens = []
    for s in sheng_sentences:
        tokens.extend(tokenize(s))
    counts = Counter(tokens)

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, count in counts.most_common():
            writer.writerow([word, count])

    print(f"Done! Word distribution saved to {OUT_FILE}")
    print(f"Total unique words: {len(counts)}")

if __name__ == "__main__":
    main()
