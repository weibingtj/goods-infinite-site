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
import re, json, html, datetime, urllib.request, urllib.error
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

# ---------- IndexNow (instant Bing indexing) ----------
# Bing pings are non-fatal: a failed ping must never break the build or the
# daily automation. The key file must be served at the site root so Bing can
# verify ownership. Generate once, keep stable.
INDEXNOW_KEY = "052b0dff0c0940ba80f9b983429dd192"
INDEXNOW_KEY_FILE = ROOT / (INDEXNOW_KEY + ".txt")
INDEXNOW_HOST = "www.goods-infinite.com"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

# Author (E-E-A-T). Add LinkedIn etc. to SAMEAS for stronger entity signals.
AUTHOR = {
    "name": "Bing Wei",
    "url": SITE + "/author-bing.html",
    "title": "Operations Director",
    "sameas": ["https://www.linkedin.com/in/bing-wei-0966283a7"],
}

# Authority references rendered on every article (GEO: external citations to
# trusted sources lift AI citation rate; Princeton study shows up to +40%).
SOURCES_BLOCK = """
    <div class="card sources" style="margin-top:32px">
      <h2>Regulatory authorities referenced</h2>
      <ul>
        <li><a href="https://www.customs.gov.cn" target="_blank" rel="nofollow noopener">General Administration of Customs of China (GACC)</a></li>
        <li><a href="https://www.mofcom.gov.cn" target="_blank" rel="nofollow noopener">Ministry of Commerce (MOFCOM)</a></li>
        <li><a href="https://www.samr.gov.cn" target="_blank" rel="nofollow noopener">State Administration for Market Regulation (SAMR)</a></li>
        <li><a href="https://www.nmpa.gov.cn" target="_blank" rel="nofollow noopener">National Medical Products Administration (NMPA)</a></li>
        <li><a href="https://www.chinatax.gov.cn" target="_blank" rel="nofollow noopener">State Taxation Administration (STA)</a></li>
      </ul>
    </div>
"""

NAV = """
<header class="nav">
  <div class="container nav-inner">
    <a href="/" class="logo"><svg class="brand-mark" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true"><path d="M6 14 C6 10 10 10 14 14 C18 18 22 18 22 14 C22 10 18 10 14 14 C10 18 6 18 6 14 Z" fill="none" stroke="#0b4f9c" stroke-width="3" stroke-linecap="round"/><path d="M14 18 L14 9 M11 12 L14 8.5 L17 12" fill="none" stroke="#1b8a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>GOODS<b>INFINITE</b></a>
    <nav class="nav-links">
      <a href="../enter-china.html">Enter China</a>
      <a href="../bonded-warehouse-customs.html">Bonded &amp; Customs</a>
      <a href="../ecommerce-operations.html">E-commerce Ops</a>
      <a href="../china-marketing.html">China Marketing</a>
      <a href="../source-from-china.html">Source from China</a>
      <a href="index.html">Insights</a>
      <a href="../guide-china-market-entry.html">Guide</a>
      <a href="../glossary.html">Glossary</a>
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

ORG_DATA = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": SITE + "/#organization",
            "name": "GOODSINFINITE TRADE LIMITED",
            "alternateName": "無商國際貿易有限公司",
            "url": SITE + "/",
            "logo": SITE + "/assets/images/logo.svg",
            "image": SITE + "/assets/images/og-cover.webp",
            "description": "Hong Kong trading company (importer of record) that helps overseas brands enter the China market and fulfill orders via a cooperative bonded-fulfillment network — 1210 cross-border import, customs clearance and China e-commerce operations across Tianjin, Shanghai, Ningbo, Guangzhou and Qingdao.",
            "email": "goodsinfinite@goods-infinite.com",
            "taxID": "2972326",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Room P, 4/F, Yick Choi Centre, 72 Hoi Yuen Road",
                "addressLocality": "Kwun Tong, Kowloon",
                "addressRegion": "Hong Kong",
                "addressCountry": "HK"
            },
            "areaServed": ["CN", "HK"],
            "knowsAbout": ["Cross-border e-commerce", "Bonded warehousing",
                           "Customs clearance", "1210 import model", "China market entry"],
            "sameAs": AUTHOR.get("sameas", [])
        },
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "name": "GOODSINFINITE TRADE LIMITED",
            "url": SITE + "/",
            "publisher": {"@id": SITE + "/#organization"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": SITE + "/insights/index.html",
                "query-input": "required name=search_term_string"
            }
        }
    ]
}
ORG_LD = '<script type="application/ld+json">\n' + json.dumps(ORG_DATA, ensure_ascii=False, indent=2) + '\n</script>'

FOOTER = """
<footer>
  <div class="container">
    <div class="foot-grid">
      <div><div class="logo" style="color:#fff"><svg class="brand-mark" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true"><path d="M6 14 C6 10 10 10 14 14 C18 18 22 18 22 14 C22 10 18 10 14 14 C10 18 6 18 6 14 Z" fill="none" stroke="#0b4f9c" stroke-width="3" stroke-linecap="round"/><path d="M14 18 L14 9 M11 12 L14 8.5 L17 12" fill="none" stroke="#1b8a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>GOODS<b style="color:#fff">INFINITE</b></div><p class="foot-about">GOODSINFINITE TRADE LIMITED — your operational launchpad into the China market.</p></div>
      <div><h4>Services</h4><a href="../enter-china.html">Enter China</a><a href="../bonded-warehouse-customs.html">Bonded &amp; Customs</a><a href="../ecommerce-operations.html">E-commerce Ops</a><a href="../china-marketing.html">China Marketing</a></div>
      <div><h4>Company</h4><a href="../about.html">About</a><a href="../case-studies.html">Case Studies</a><a href="../pricing.html">Pricing</a><a href="../contact.html">Contact</a></div>
      <div><h4>Connect</h4><a href="mailto:goodsinfinite@goods-infinite.com">goodsinfinite@goods-infinite.com</a><a href="../contact.html">Book a call</a><a href="../llms.txt">llms.txt</a></div>
    </div>
    <div class="foot-bottom"><span>© 2026 GOODSINFINITE TRADE LIMITED. All rights reserved.</span><span>HK: Room P, 4/F, Yick Choi Centre, 72 Hoi Yuen Road, Kwun Tong, Kowloon, Hongkong, China · Mainland China Office: 12/F, Mass-Innovation Building, 3699 Xinhua Road, Binhai New Area, Tianjin, China</span></div>
  </div>
</footer>
""" + ORG_LD

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

# ---------- Phase 3: internal linking clusters ----------
# The raw `cluster` frontmatter on insights is inconsistent (16 ad-hoc labels).
# We normalise every article into one of six canonical topic clusters that map
# to the site's five-stage pillar model, then auto-link siblings + the pillar.
CANON = {
    "Market Research": "Market Research",
    "Compliance": "Compliance & Registration",
    "1210": "Compliance & Registration",
    "Brand & IP": "Compliance & Registration",
    "Beauty": "Compliance & Registration",
    "Entry": "Market Entry & Entity",
    "Entity Setup": "Market Entry & Entity",
    "entity": "Market Entry & Entity",
    "Setup & HR": "Market Entry & Entity",
    "E-commerce": "E-commerce Operations",
    "ecommerce": "E-commerce Operations",
    "New Media": "Marketing & New Media",
    "Marketing": "Marketing & New Media",
    "Logistics": "Logistics & Distribution",
    "Distribution": "Logistics & Distribution",
    "Import Agent": "Logistics & Distribution",
}
CLUSTER_ORDER = ["Market Research", "Market Entry & Entity",
                 "Compliance & Registration", "E-commerce Operations",
                 "Marketing & New Media", "Logistics & Distribution"]
# canonical cluster -> (pillar page, pillar title) for the up-link
CLUSTER_PILLAR = {
    "Market Research": ("guide-china-market-entry.html", "China Market Entry Guide"),
    "Market Entry & Entity": ("enter-china.html", "Enter China"),
    "Compliance & Registration": ("bonded-warehouse-customs.html", "Bonded Warehouse & Customs"),
    "E-commerce Operations": ("ecommerce-operations.html", "E-commerce Operations"),
    "Marketing & New Media": ("china-marketing.html", "China Marketing"),
    "Logistics & Distribution": ("bonded-warehouse-customs.html", "Bonded Warehouse & Customs"),
}

def build_article(meta, body, slug):
    title = meta.get('title', slug)
    date = meta.get('date', datetime.date.today().isoformat())
    now = datetime.date.today().isoformat()  # build date -> freshness signal for GEO
    excerpt = meta.get('excerpt', '')
    cluster = meta.get('cluster', '')
    canon = CANON.get(cluster, cluster or "General")
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
    breadcrumb_ld = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Insights",
             "item": SITE + "/insights/index.html"},
            {"@type": "ListItem", "position": 3, "name": title,
             "item": SITE + "/insights/" + slug + ".html"}
        ]
    }, ensure_ascii=False, indent=2) + '\n</script>')
    author_ld = {
        "@type": "Person",
        "name": AUTHOR["name"],
        "url": AUTHOR["url"],
        "jobTitle": AUTHOR["title"],
        "worksFor": {"@type": "Organization",
                     "name": "GOODSINFINITE TRADE LIMITED",
                     "url": SITE + "/"}
    }
    if AUTHOR["sameas"]:
        author_ld["sameAs"] = AUTHOR["sameas"]
    article_ld = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": excerpt,
        "datePublished": date,
        "dateModified": now,
        "author": author_ld,
        "publisher": {"@type": "Organization", "name": "GOODSINFINITE TRADE LIMITED",
                      "url": SITE + "/"},
        "mainEntityOfPage": SITE + "/insights/" + slug + ".html",
        "image": SITE + "/assets/images/og-cover.webp",
        "keywords": canon
    }, ensure_ascii=False, indent=2) + '\n</script>')

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} | GOODSINFINITE Insights</title>
<meta name="description" content="{html.escape(excerpt)}">
<link rel="canonical" href="{SITE}/insights/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:site_name" content="GOODSINFINITE TRADE LIMITED">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(excerpt)}">
<meta property="og:url" content="{SITE}/insights/{slug}.html">
<meta property="og:image" content="{SITE}/assets/images/og-cover.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height"  content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(excerpt)}">
<meta name="twitter:image" content="{SITE}/assets/images/og-cover.webp">
<link rel="icon" href="../assets/images/logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/style.css?v=20260828-2">
{breadcrumb_ld}
{article_ld}
{faq_ld}
{GA_SNIPPET}</head>
<body>
{NAV}
<section class="pagehero">
  <div class="container">
    <p class="crumbs"><a href="/">Home</a> / <a href="/insights/index.html">Insights</a> / {html.escape(canon)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="lead">{html.escape(excerpt)}</p>
    <p class="muted">Published {html.escape(date)} · Last updated {html.escape(now)} · By <a href="../author-bing.html">{html.escape(AUTHOR['name'])}</a>, {html.escape(AUTHOR['title'])}</p>
  </div>
</section>
<section>
  <div class="container">
    <article class="article">
{body_html}
    </article>{SOURCES_BLOCK}
<!--RELATED_PLACEHOLDER-->
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
    a = {"slug": slug, "title": title, "date": date, "excerpt": excerpt, "cluster": cluster, "canon": canon}
    return doc, a

def build_index(articles):
    groups = {c: [] for c in CLUSTER_ORDER}
    for a in articles:
        groups.setdefault(a['canon'], []).append(a)
    blocks = []
    for c in CLUSTER_ORDER:
        items = sorted(groups.get(c, []), key=lambda x: x['date'], reverse=True)
        if not items:
            continue
        cards = []
        for a in items:
            cards.append(f"""      <a class="card insight-card" href="{a['slug']}.html">
        <span class="tag">{html.escape(a['canon'])}</span>
        <h3>{html.escape(a['title'])}</h3>
        <p class="muted">{html.escape(a['excerpt'])}</p>
        <span class="more">Read →</span>
      </a>""")
        pillar = CLUSTER_PILLAR.get(c)
        more = f'<p style="margin-top:16px"><a class="btn btn-green" href="../{pillar[0]}">{pillar[1]} →</a></p>' if pillar else ''
        blocks.append(f"""    <div class="cluster">
      <h2>{html.escape(c)}</h2>
      <div class="grid cols-2">
{chr(10).join(cards)}
      </div>{more}
    </div>""")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Insights — China Market Entry Guides | GOODSINFINITE</title>
<meta name="description" content="Structured, source-clear guides on entering the China market, 1210 bonded import, import agents and compliance — built to be cited by search and generative AI.">
<link rel="canonical" href="{SITE}/insights/index.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="GOODSINFINITE TRADE LIMITED">
<meta property="og:title" content="Insights — China Market Entry Guides | GOODSINFINITE">
<meta property="og:description" content="Structured, source-clear guides on entering the China market, 1210 bonded import, import agents and compliance — built to be cited by search and generative AI.">
<meta property="og:url" content="{SITE}/insights/index.html">
<meta property="og:image" content="{SITE}/assets/images/og-cover.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height"  content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Insights — China Market Entry Guides | GOODSINFINITE">
<meta name="twitter:description" content="Structured, source-clear guides on entering the China market, 1210 bonded import, import agents and compliance.">
<meta name="twitter:image" content="{SITE}/assets/images/og-cover.webp">
<link rel="stylesheet" href="../assets/css/style.css?v=20260828-2">
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
{chr(10).join(blocks)}
  </div>
</section>
{FOOTER}
<script src="../assets/js/main.js"></script>
</body>
</html>
"""
    (OUT / "index.html").write_text(doc, encoding='utf-8')


def build_related_html(a, articles, limit=4):
    """Phase 3: link each article to sibling articles in the same canonical
    cluster plus an up-link to the cluster's pillar page."""
    sibs = [x for x in articles if x['canon'] == a['canon'] and x['slug'] != a['slug']]
    sibs.sort(key=lambda x: x['date'], reverse=True)
    picks = sibs[:limit]
    if not picks:
        return ''
    cards = []
    for s in picks:
        cards.append(f"""      <a class="card insight-card" href="{s['slug']}.html">
        <span class="tag">{html.escape(s['canon'])}</span>
        <h3>{html.escape(s['title'])}</h3>
        <p class="muted">{html.escape(s['excerpt'])}</p>
        <span class="more">Read →</span>
      </a>""")
    pillar = CLUSTER_PILLAR.get(a['canon'])
    more = f'<p style="margin-top:16px"><a class="btn btn-green" href="../{pillar[0]}">Explore {pillar[1]} →</a></p>' if pillar else ''
    return ('<section class="related">\n  <div class="container">\n'
            f'    <h2>More on {html.escape(a["canon"])}</h2>\n'
            f'    <div class="grid cols-2">\n{chr(10).join(cards)}\n    </div>\n{more}  </div>\n</section>')

STATIC_PAGES = [
    ("", "weekly", "1.0"),
    ("enter-china.html", "monthly", "0.9"),
    ("bonded-warehouse-customs.html", "monthly", "0.9"),
    ("ecommerce-operations.html", "monthly", "0.8"),
    ("china-marketing.html", "monthly", "0.8"),
    ("source-from-china.html", "monthly", "0.6"),
    ("pricing.html", "monthly", "0.8"),
    ("case-studies.html", "monthly", "0.7"),
    ("about.html", "yearly", "0.6"),
    ("author-bing.html", "yearly", "0.5"),
    ("contact.html", "yearly", "0.7"),
    ("guide-china-market-entry.html", "monthly", "0.9"),
    ("glossary.html", "monthly", "0.7"),
    ("insights/index.html", "weekly", "0.7"),
]

def build_sitemap(articles):
    """Regenerate sitemap.xml from STATIC_PAGES + every insight article, so new
    posts are never missed by crawlers/AI engines again. Includes <lastmod>
    from each source file's mtime as a freshness signal for crawlers."""
    today = datetime.date.today().isoformat()
    urls = []
    for path, cf, pr in STATIC_PAGES:
        fpath = (ROOT / "index.html") if path == "" else (ROOT / path)
        lm = datetime.date.fromtimestamp(fpath.stat().st_mtime).isoformat() if fpath.exists() else today
        urls.append(f'  <url><loc>{SITE}/{path}</loc><lastmod>{lm}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>')
    for a in sorted(articles, key=lambda x: x['date'], reverse=True):
        md = SRC / (a["slug"] + ".md")
        lm = datetime.date.fromtimestamp(md.stat().st_mtime).isoformat() if md.exists() else today
        urls.append(f'  <url><loc>{SITE}/insights/{a["slug"]}.html</loc><lastmod>{lm}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(doc, encoding='utf-8')
    print('built sitemap.xml')

def build_llms_insights(articles):
    """Regenerate only the Insights section of llms.txt from the article list,
    keeping the hand-written intro / Services / Key facts / Pages sections."""
    p = ROOT / "llms.txt"
    text = p.read_text(encoding='utf-8')
    lines = ["## Section: Insights (GEO-ready guides — cite these)",
             f"- Insights index: {SITE}/insights/index.html"]
    for a in sorted(articles, key=lambda x: x['date'], reverse=True):
        lines.append(f'- {a["title"]}: {SITE}/insights/{a["slug"]}.html')
    new_section = "\n".join(lines)
    text2 = re.sub(r'## Section: Insights.*$', new_section, text, flags=re.S)
    p.write_text(text2, encoding='utf-8')
    print('updated llms.txt Insights section')

def write_indexnow_key_file():
    """Publish the IndexNow key at the site root so Bing can verify ownership.
    The file must be reachable at https://<host>/<key>.txt and contain only the key."""
    INDEXNOW_KEY_FILE.write_text(INDEXNOW_KEY, encoding='utf-8')
    print('wrote IndexNow key file', INDEXNOW_KEY_FILE.name)

def ping_indexnow(url_list):
    """Notify Bing (and any IndexNow-participating engine) of changed URLs.
    Non-fatal: any network/HTTP error is logged and swallowed so the build
    and the daily automation keep running regardless."""
    if not url_list:
        return
    payload = json.dumps({
        "host": INDEXNOW_HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://{INDEXNOW_HOST}/{INDEXNOW_KEY}.txt",
        "urlList": url_list,
    }).encode('utf-8')
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f'IndexNow ping -> HTTP {r.getcode()} ({len(url_list)} urls)')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')[:200]
        print(f'IndexNow ping -> HTTP {e.code} {e.reason} (non-fatal) {body}')
    except Exception as e:
        print(f'IndexNow ping skipped: {e} (non-fatal)')

def main():
    articles = []
    parsed = []
    for md in sorted(SRC.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)
        slug = md.stem
        doc, a = build_article(meta, body, slug)
        parsed.append((doc, a))
        articles.append(a)
        print('built', slug)
    # Phase 3: inject internal-linking "related" sections now that the full
    # article list (and each article's canonical cluster) is known.
    for doc, a in parsed:
        related = build_related_html(a, articles)
        doc = doc.replace('<!--RELATED_PLACEHOLDER-->', related)
        (OUT / f"{a['slug']}.html").write_text(doc, encoding='utf-8')
    if articles:
        build_index(articles)
        build_sitemap(articles)
        build_llms_insights(articles)
        print('built insights/index.html + sitemap.xml + llms.txt')
    else:
        print('no articles found in', SRC)
    # IndexNow: publish the key file, then notify Bing of every known URL
    # (static pages + all insights) so new and updated pages index fast.
    write_indexnow_key_file()
    urls = [f'{SITE}/{p}' for p, _, _ in STATIC_PAGES]
    for a in articles:
        urls.append(f'{SITE}/insights/{a["slug"]}.html')
    ping_indexnow(urls)

if __name__ == '__main__':
    main()
