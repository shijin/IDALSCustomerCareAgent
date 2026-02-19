import csv
from langchain_core.documents import Document

def load_faq_csv(path: str):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            docs.append(
                Document(page_content=f"Q: {row[0]}\nA: {row[1]}")
            )
    return docs
