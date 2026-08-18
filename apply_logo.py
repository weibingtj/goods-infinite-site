from pathlib import Path
root = Path(r'E:/workbuddy/2026-08-18-12-10-21/goodsinfinite')

MARK = ('<svg class="brand-mark" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true">'
        '<path d="M6 14 C6 10 10 10 14 14 C18 18 22 18 22 14 C22 10 18 10 14 14 C10 18 6 18 6 14 Z" '
        'fill="none" stroke="#0b4f9c" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M14 18 L14 9 M11 12 L14 8.5 L17 12" '
        'fill="none" stroke="#1b8a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
DOT = '<span class="dot"></span>'
FAV = '<link rel="icon" href="assets/images/logo.svg" type="image/svg+xml">\n  <link rel="stylesheet" href="assets/css/style.css">'

for p in sorted(root.glob('*.html')):
    t = p.read_text(encoding='utf-8')
    t = t.replace(DOT, MARK, 1)
    t = t.replace('<div class="logo" style="color:#fff"><span class="dot"></span>GOODS<b style="color:#fff">INFINITE</b></div>',
                  '<div class="logo" style="color:#fff">' + MARK + 'GOODS<b style="color:#fff">INFINITE</b></div>')
    if 'rel="icon"' not in t:
        t = t.replace('<link rel="stylesheet" href="assets/css/style.css">', FAV, 1)
    p.write_text(t, encoding='utf-8')
    print('updated', p.name)

bs = root / 'build_insights.py'
b = bs.read_text(encoding='utf-8')
b = b.replace('<a href="../index.html" class="logo"><span class="dot"></span>GOODS<b>INFINITE</b></a>',
              '<a href="../index.html" class="logo">' + MARK + 'GOODS<b>INFINITE</b></a>')
b = b.replace('<div class="logo" style="color:#fff"><span class="dot"></span>GOODS<b style="color:#fff">INFINITE</b></div>',
              '<div class="logo" style="color:#fff">' + MARK + 'GOODS<b style="color:#fff">INFINITE</b></div>')
if 'rel="icon"' not in b:
    b = b.replace('<link rel="stylesheet" href="../assets/css/style.css">',
                  '<link rel="icon" href="../assets/images/logo.svg" type="image/svg+xml">\n  <link rel="stylesheet" href="../assets/css/style.css">', 1)
bs.write_text(b, encoding='utf-8')
print('updated build_insights.py')
