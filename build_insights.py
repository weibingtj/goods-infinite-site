#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOODSINFINITE Insights builder (stdlib only — zero pip install for deploy).
Reads markdown articles from content/insights/*.md (frontmatter + body),
renders a full static HTML page per article into insights/, and regenerates
insights/index.html. Decap CMS edits the markdown; this script publishes it.

Usage:  python build_insights.py
Deploy: set the Cloudflare Pages build command to `python build_insights.py`.
"""
import re, json, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# GA4 snippet (kept as a plain string so it can sit inside f-strings safely)
GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-68HRE7BJFK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-68HRE7BJFK');
</script>
"""
SRC = ROOT / "content" / "insights"
OUT = ROOT / "insights"
OUT.mkdir(parents=True, exist_ok=True)

SITE = "https://www.goods-infinite.com"

NAV = """
<header class="nav">
  <div class="container nav-inner">
    <a href="../index.html" class="logo"><svg class="brand-mark" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true"><path d="M6 14 C6 10 10 10 14 14 C18 18 22 18 22 14 C22 10 18 10 14 14 C10 18 6 18 6 14 Z" fill="none" stroke="#0b4f9c" stroke-width="3" stroke-linecap="round"/><path d="M14 18 L14 9 M11 12 L14 8.5 L17 12" fill="none" stroke="#1b8a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>GOODS<b>INFINITE</b></a>
    <nav class="nav-links">
      <a href="../enter-china.html">Enter China</a>
      <a href="../bonded-warehouse-customs.html">Bonded &amp; Customs</a>
      <a href="../ecommerce-operations.html">E-commerce Ops</a>
      <a href="../china-marketing.html">China Marketing</a>
      <a href="../source-from-china.html">Source from China</a>
      <a href="index.html">Insights</a>
      <a href="../pricing.html">Pricing</a>
      <a href="../about.html">About</a>
      <a href="../contact.html" class="btn">Contact</a>
    </nav>
    <button class="hamburger" id="navToggle" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="../enter-china.html">Enter China</a>
    <a href="../bonded-warehouse-customs.html">Bonded &amp; Customs</a>
    <a href="../ecommerce-operations.html">E-commerce Ops</a>
    <a href="../china-marketing.html">China Marketing</a>
    <a href="../source-from-china.html">Source from China</a>
    <a href="index.html">Insights</a>
    <a href="../pricing.html">Pricing</a>
    <a href="../about.html">About</a>
    <a href="../contact.html">Contact</a>
  </div>
</header>
"""

FOOTER = """
<footer>
  <div class="container">
    <div class="foot-grid">
      <div><div class="logo" style="color:#fff"><svg class="brand-mark" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true"><path d="M6 14 C6 10 10 10 14 14 C18 18 22 18 22 14 C22 10 18 10 14 14 C10 18 6 18 6 14 Z" fill="none" stroke="#0b4f9c" stroke-width="3" stroke-linecap="round"/><path d="M14 18 L14 9 M11 12 L14 8.5 L17 12" fill="none" stroke="#1b8a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>GOODS<b style="color:#fff">INFINITE</b></div><p class="foot-about">GOODSINFINITE TRADE LIMITED — your operational launchpad into the China market.</p></div>
      <div><h4>Services</h4><a href="../enter-china.html">Enter China</a><a href="../bonded-warehouse-customs.html">Bonded &amp; Customs</a><a href="../ecommerce-operations.html">E-commerce Ops</a><a href="../china-marketing.html">China Marketing</a></div>
      <div><h4>Company</h4><a href="../about.html">About</a><a href="../case-studies.html">Case Studies</a><a href="../pricing.html">Pricing</a><a href="../contact.html">Contact</a></div>
      <div><h4>Connect</h4><a href="mailto:goodsinfinite@goods-infinite.com">goodsinfinite@goods-infinite.com</a><a href="../contact.html">Book a call</a><a href="../llms.txt">llms.txt</a></div>
    </div>
    <div class="foot-bottom"><span>© 2026 GOODSINFINITE TRADE LIMITED. All rights reserved.</span><span>HK: Room P, 4/F, Yick Choi Centre, 72 Hoi Yuen Road, Kwun Tong, Kowloon, HK · China office: 12/F, Mass-Innovation Building, 3699 Xinhua Road, Binhai New Area, Tianjin, China</span></div>
  </div>
</footer>
"""

# ---------- markdown -> html (minimal, dependency-free) ----------
def inline(s):
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    return s

def md_to_html(md):
    lines = md.split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.strip() == '':
            i += 1; continue
        if line.strip().startswith('<'):  # raw HTML block (tables etc.)
            block = []
            while i < n and lines[i].strip() != '':
                block.append(lines[i]); i += 1
            out.append('\n'.join(block)); continue
        if line.startswith('## '):
            out.append(f'<h2>{inline(line[3:].strip())}</h2>'); i += 1; continue
        if line.startswith('### '):
            out.append(f'<h3>{inline(line[4:].strip())}</h3>'); i += 1; continue
        if line.startswith('# '):
            out.append(f'<h1>{inline(line[2:].strip())}</h1>'); i += 1; continue
        if line.strip() == '---':
            out.append('<hr>'); i += 1; continue
        if line.startswith('> '):
            q = []
            while i < n and lines[i].startswith('> '):
                q.append(lines[i][2:]); i += 1
            out.append(f'<blockquote>{inline(" ".join(q))}</blockquote>'); continue
        if re.match(r'^\s*[-*]\s', line):
            items = []
            while i < n and re.match(r'^\s*[-*]\s', lines[i]):
                items.append(re.sub(r'^\s*[-*]\s', '', lines[i])); i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(it)}</li>' for it in items) + '</ul>'); continue
        if re.match(r'^\s*\d+\.\s', line):
            items = []
            while i < n and re.match(r'^\s*\d+\.\s', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s', '', lines[i])); i += 1
            out.append('<ol>' + ''.join(f'<li>{inline(it)}</li>' for it in items) + '</ol>'); continue
        # paragraph
        para = []
        while (i < n and lines[i].strip() != ''
               and not lines[i].startswith('# ')
               and not lines[i].startswith('> ')
               and not lines[i].strip().startswith('<')
               and not re.match(r'^\s*[-*]\s', lines[i])
               and not re.match(r'^\s*\d+\.\s', lines[i])
               and lines[i].strip() != '---'):
            para.append(lines[i]); i += 1
        out.append(f'<p>{inline(" ".join(para))}</p>')
    return '\n'.join(out)

# ---------- frontmatter ----------
def parse_frontmatter(text):
    if not text.startswith('---'):
        raise ValueError('Missing frontmatter')
    parts = text.split('---', 2)
    fm_raw, body = parts[1], parts[2].lstrip('\n')
    meta = {}
    faq = []
    mode = None
    cur = None
    for ln in fm_raw.split('\n'):
        if ln.strip() == '':
            continue
        m = re.match(r'^(\w[\w-]*):\s*(.*)$', ln)
        if m and not ln.startswith(' '):
            key, val = m.group(1), m.group(2).strip()
            if val == '':
                mode = key if key == 'faq' else None
                if key != 'faq':
                    meta[key] = ''
                continue
            meta[key] = val.strip('"')
            mode = None
            continue
        if mode == 'faq':
            q = re.match(r'^\s*-\s*q:\s*(.*)$', ln)
            a = re.match(r'^\s*a:\s*(.*)$', ln)
            if q:
                cur = {'q': q.group(1).strip()}; faq.append(cur)
            elif a and cur is not None:
                cur['a'] = a.group(1).strip()
    meta['faq'] = faq
    return meta, body

def build_article(meta, body, slug):
    title = meta.get('title', slug)
    date = meta.get('date', datetime.date.today().isoformat())
    excerpt = meta.get('excerpt', '')
    cluster = meta.get('cluster', '')
    body_html = md_to_html(body)
    faq = meta.get('faq', [])
    faq_ld = ''
    if faq:
        faq_ld = ('<script type="application/ld+json">\n' + json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q['q'],
                            "acceptedAnswer": {"@type": "Answer", "text": q['a']}}
                           for q in faq if 'q' in q and 'a' in q]
        }, ensure_ascii=False, indent=2) + '\n</script>')
    article_ld = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": excerpt,
        "datePublished": date,
        "author": {"@type": "Organization", "name": "GOODSINFINITE TRADE LIMITED"},
        "publisher": {"@type": "Organization", "name": "GOODSINFINITE TRADE LIMITED",
                      "url": SITE + "/"},
        "mainEntityOfPage": SITE + "/insights/" + slug + ".html",
        "keywords": cluster
    }, ensure_ascii=False, indent=2) + '\n</script>')

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} | GOODSINFINITE Insights</title>
<meta name="description" content="{html.escape(excerpt)}">
<link rel="canonical" href="{SITE}/insights/{slug}.html">
<link rel="icon" href="../assets/images/logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/style.css">
{article_ld}
{faq_ld}
{GA_SNIPPET}</head>
<body>
{NAV}
<section class="pagehero">
  <div class="container">
    <p class="crumbs"><a href="index.html">Insights</a> / {html.escape(cluster)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="lead">{html.escape(excerpt)}</p>
    <p class="muted">Published {html.escape(date)} · GOODSINFINITE TRADE LIMITED</p>
  </div>
</section>
<section>
  <div class="container">
    <article class="article">
{body_html}
    </article>
    <div class="ctaband" style="margin-top:40px">
      <h2>Talk to our China entry team</h2>
      <p>Have a question about your product's path into China? Book a free 30-minute call.</p>
      <a href="../contact.html" class="btn btn-green">Book a call</a>
    </div>
  </div>
</section>
{FOOTER}
<script src="../assets/js/main.js"></script>
</body>
</html>
"""
    (OUT / f"{slug}.html").write_text(doc, encoding='utf-8')
    return {"slug": slug, "title": title, "date": date, "excerpt": excerpt, "cluster": cluster}

def build_index(articles):
    cards = []
    for a in sorted(articles, key=lambda x: x['date'], reverse=True):
        cards.append(f"""      <a class="card insight-card" href="{a['slug']}.html">
        <span class="tag">{html.escape(a['cluster'])}</span>
        <h3>{html.escape(a['title'])}</h3>
        <p class="muted">{html.escape(a['excerpt'])}</p>
        <span class="more">Read →</span>
      </a>""")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Insights — China Market Entry Guides | GOODSINFINITE</title>
<meta name="description" content="Structured, source-clear guides on entering the China market, 1210 bonded import, import agents and compliance — built to be cited by search and generative AI.">
<link rel="canonical" href="{SITE}/insights/index.html">
<link rel="stylesheet" href="../assets/css/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"GOODSINFINITE Insights","url":"{SITE}/insights/index.html"}}
</script>
{GA_SNIPPET}</head>
<body>
{NAV}
<section class="pagehero">
  <div class="container">
    <p class="crumbs">Home / Insights</p>
    <h1>Insights on entering the China market</h1>
    <p class="lead">Practical, structured guides on the questions overseas brands actually ask — written to be useful to you and quotable by AI search engines alike.</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="grid cols-2">
{chr(10).join(cards)}
    </div>
  </div>
</section>
{FOOTER}
<script src="../assets/js/main.js"></script>
</body>
</html>
"""
    (OUT / "index.html").write_text(doc, encoding='utf-8')

def main():
    articles = []
    for md in sorted(SRC.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)
        slug = md.stem
        a = build_article(meta, body, slug)
        articles.append(a)
        print('built', slug)
    if articles:
        build_index(articles)
        print('built insights/index.html')
    else:
        print('no articles found in', SRC)

if __name__ == '__main__':
    main()
