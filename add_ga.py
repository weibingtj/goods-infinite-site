import os, io

ROOT = os.path.dirname(os.path.abspath(__file__))
GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-68HRE7BJFK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-68HRE7BJFK');
</script>
"""

MARKER = "googletagmanager.com/gtag/js?id=G-68HRE7BJFK"
SKIP = {os.path.join(ROOT, "admin", "index.html"),
        os.path.join(ROOT, "google33bc9d4e74be2ca0.html")}

count = 0
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        if fp in SKIP:
            continue
        with io.open(fp, "r", encoding="utf-8") as f:
            html = f.read()
        if MARKER in html:
            continue
        if "</head>" not in html:
            continue
        html = html.replace("</head>", GA_SNIPPET + "\n</head>", 1)
        with io.open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print("injected:", os.path.relpath(fp, ROOT))
print("TOTAL injected:", count)
