import pdfplumber, re, sys
PDF = r"C:\Users\Administrator\Downloads\Katrina Product Cataloge DC, DK, Candy minis&bars.pdf"
out = r"E:\workbuddy\2026-08-18-12-10-21\goodsinfinite\images\_src\catalog_text.txt"
alltext = []
with pdfplumber.open(PDF) as pdf:
    print("PAGES:", len(pdf.pages))
    for i, page in enumerate(pdf.pages):
        t = page.extract_text() or ""
        alltext.append(f"===== PAGE {i+1} =====\n{t}")
print("CHARS:", sum(len(x) for x in alltext))
with open(out, "w", encoding="utf-8") as f:
    f.write("\n\n".join(alltext))
# print a trimmed dump to console
full = "\n\n".join(alltext)
print(full[:6000])
