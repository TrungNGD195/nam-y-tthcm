"""Reproducible local extraction. Source PDFs stay outside the public build."""
from pathlib import Path
import json
import re
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "materials/tthcm"
OUTPUT = ROOT / "content/tthcm"
OUTPUT.mkdir(exist_ok=True)

def clean(text):
    text = text.replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"\[!info:\d+\]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def parse(filename, source_id, chapters):
    doc = pymupdf.open(SOURCE / filename)
    text = ""
    starts = []
    for page in doc:
        starts.append(len(text))
        text += page.get_text(sort=True).replace("\u200b", "") + "\n"
    markers = list(re.finditer(r"(?m)^\s*(?:Câu\s*)?(\d+)\s*[.:]\s*", text))
    group = 0
    previous = 0
    result = []
    for index, marker in enumerate(markers):
        number = int(marker.group(1))
        if index and number < previous:
            group += 1
        previous = number
        body = text[marker.end():markers[index+1].start() if index+1 < len(markers) else len(text)]
        options = list(re.finditer(r"(?m)^\s*(\*?)\s*([A-D])\s*[.)]\s*", body))
        prompt = body[:options[0].start()] if options else body
        choices = []
        correct = None
        for j, option in enumerate(options):
            letter = option.group(2).lower()
            value = body[option.end():options[j+1].start() if j+1 < len(options) else len(body)]
            choices.append({"id": letter, "text": clean(value)})
            if option.group(1):
                correct = letter
        chapter = chapters[group] if isinstance(chapters, list) else chapters.get(number)
        page = max(i+1 for i, start in enumerate(starts) if start <= marker.end())
        ident = f"{source_id}-g{group+1}-{number:02d}"
        result.append({"id": ident, "sourceId": source_id, "chapter": chapter, "group": group+1,
                       "originalNumber": number, "pdfPage": page, "prompt": clean(prompt),
                       "options": choices, "markedAnswer": correct, "originalText": clean(body)})
    return result

raw = []
raw += parse("TTHCM LMS.pdf", "lms", [1,2,3,4,5,6])
raw += parse("Quiz cô Khánh.pdf", "quiz", [1,2,2,2,3,4,5,6])
raw += parse("Đề mẫu 20 câu Thầy Cường.docx.pdf", "sample", {
    3:1, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2, 10:1, 11:2, 12:2,
    13:3, 14:3, 15:5, 16:5, 17:2, 18:6, 19:3, 20:6, 21:3, 22:2})
(OUTPUT / "raw-questions.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Extracted {len(raw)} source items.")
for q in raw:
    print(f"{q['id']:17} c{q['chapter']} p{q['pdfPage']:2} ({len(q['options'])}) {q['prompt'][:155]}")
    if q['sourceId'] != 'lms':
        print("  " + " | ".join(f"{o['id']}: {o['text'][:100]}" for o in q['options']))
