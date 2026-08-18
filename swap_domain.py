from pathlib import Path

root = Path(r'E:/workbuddy/2026-08-18-12-10-21/goodsinfinite')
OLD = "www.goods-infinite.com"
NEW = "www.goods-infinite.com"

count = 0
files = []
for p in root.rglob('*'):
    if p.is_file() and p.suffix in {'.html', '.xml', '.txt', '.py', '.yml', '.md', '.json'}:
        try:
            t = p.read_text(encoding='utf-8')
        except Exception:
            continue
        if OLD in t:
            t2 = t.replace(OLD, NEW)
            p.write_text(t2, encoding='utf-8')
            count += t.count(OLD)
            files.append(p.name)

print(f"Replaced {count} occurrences across {len(files)} files.")
for f in sorted(set(files)):
    print(" -", f)
