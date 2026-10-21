---
title: "China PIPL & Data Compliance for Cross-Border E-Commerce: The 2026 Rules for Foreign Brands"
slug: "china-pipl-data-compliance-cross-border-ecommerce"
date: "2026-10-21"
excerpt: "Selling to Chinese consumers through 1210 bonded or 9610 direct-mail means you are processing Chinese personal information — whether or not you have a Chinese entity. Here is what PIPL actually requires, the three export gateways, the exemption most cross-border sellers can use, and the filings you cannot skip."
cluster: "Compliance"
keywords:
  - China PIPL
  - data compliance China cross-border ecommerce
  - personal information export China
  - 1210 bonded data compliance
  - China data export security assessment
faq:
  - q: "Does China's PIPL apply to my brand if I have no Chinese entity and only sell through cross-border e-commerce?"
    a: "Yes. PIPL Article 3(2) applies the law to processing of Chinese residents' personal information carried out outside China where the purpose is to provide products or services to individuals in China, or to analyse or assess their behaviour. Selling into China through Tmall Global, JD Worldwide or Douyin cross-border is squarely 'providing products or services to individuals in China', so PIPL applies to the overseas brand even with no mainland company."
  - q: "Do I need a data export security assessment to send Chinese customer data to my head office?"
    a: "Usually not. Under CAC Order No. 16 (Article 5(1)), personal information provided overseas where necessary to conclude or perform a contract to which the individual is a party — expressly including cross-border shopping — is exempt from security assessment, standard contract and certification. Separately, non-CIIO processors exporting under 100,000 individuals' non-sensitive personal information since 1 January of the current year are also exempt. Assessment is only mandatory above 1 million individuals, or 10,000 individuals' sensitive personal information."
  - q: "What personal data actually has to be sent to Chinese customs on a cross-border order?"
    a: "For each cross-border retail import order the platform or the overseas seller's mainland agent, the payment company and the logistics company each transmit order, payment and logistics electronic data to customs through the Single Window for the 'three-document' (三单) match, and bear responsibility for data authenticity (GACC Announcement No. 194 of 2018). The buyer's name and ID number are part of that flow, and customs runs a separate buyer identity verification — the consumer confirms via face recognition in the 'Customs on Hand' or 'Single Window on Hand' app."
  - q: "Do I have to appoint a China-based representative for personal information protection?"
    a: "If you are an overseas personal information processor caught by PIPL Article 3(2), yes. Article 53 requires you to establish a dedicated body in China or designate a representative to handle personal information protection matters, and to file that body's name or the representative's name and contact details with the competent authority. The Network Data Security Management Regulation (Article 26) specifies the filing goes to the municipal-level cyberspace administration where the body or representative is located."
  - q: "Even if my data export is exempt, do any obligations remain?"
    a: "Yes, and this is the most commonly missed point. CAC Order No. 16 Article 10 makes clear that a processor providing personal information overseas must still perform notification, obtain the individual's separate consent, and conduct a personal information protection impact assessment under PIPL. The exemption removes the assessment/contract/certification gateway — it does not remove transparency, consent or accountability duties."
  - q: "What are the penalties for getting this wrong?"
    a: "Under PIPL Article 66, a processor that fails to correct after an order may be fined up to RMB 1 million, with RMB 10,000–100,000 on responsible individuals; for serious cases the ceiling rises to RMB 50 million or 5% of the previous year's turnover, business may be suspended, licences revoked, and responsible individuals face RMB 100,000–1,000,000 plus a bar on serving as director, supervisor, senior manager or personal information protection officer."
---

## Definition: what "China data compliance for cross-border e-commerce" actually means

"China data compliance for cross-border e-commerce" is the set of obligations a foreign brand takes on the moment it **collects, stores, uses or moves out of China the personal information of Chinese buyers** — order data, name, ID number, phone, address, payment and logistics records — in the course of selling into China through bonded (1210) or direct-mail (9610) channels, or through a domestic store once it has a mainland entity.

The critical thing most overseas sellers get wrong: **this is not a "China entity" question.** China's Personal Information Protection Law has explicit extraterritorial reach. If you have no WFOE, no office and no staff in mainland China but you sell to Chinese consumers, PIPL still governs you — and the practical consequence is not just a privacy policy rewrite, but decisions about **where your data sits, what crosses the border, and who in China is answerable for it.**

<div class="statcard"><span class="n">RMB 50m / 5%</span><span class="l">The maximum fine for a serious PIPL violation: RMB 50 million or 5% of the previous year's turnover, whichever applies, plus suspension of the relevant business, revocation of the business licence, and RMB 100,000–1,000,000 on the responsible individuals — who can also be barred from serving as a director, supervisor, senior manager or personal information protection officer</span><span class="src">Source: Personal Information Protection Law, Art. 66</span></div>

## Step 1 — Establish whether PIPL reaches you at all

PIPL Article 3 has two limbs:

- **Art. 3(1)** — processing personal information *within* China.
- **Art. 3(2)** — processing the personal information of individuals in China *from outside* China, where the purpose is **(a) providing products or services to individuals in China**, **(b) analysing or assessing their behaviour**, or (c) other circumstances set out in laws and regulations.

A foreign brand selling into China through cross-border e-commerce meets limb (a) by definition. So does running Chinese-language performance marketing, retargeting Chinese audiences, or maintaining a Chinese-language customer database.

> The moment you ship a 1210 order, you are a "personal information processor" under Chinese law. There is no de-minimis threshold, no "we only have 200 customers" carve-out and no "our server is in Frankfurt" defence.

## Step 2 — Work out who holds which role in a cross-border transaction

Chinese law does not treat "the seller" as a single data controller. Under the six-ministry notice that governs cross-border retail imports (商财发〔2018〕486号), a 1210/9610 transaction has four defined participants, each with distinct duties:

| Participant | Who they are | Data / compliance duty |
|---|---|---|
| **Cross-border e-commerce enterprise** | The **overseas-registered** company selling to Chinese consumers; owner of the goods | Bears product-quality and consumer-rights responsibility; **must entrust one mainland-registered enterprise** to register with customs, file truthfully and bear joint and several civil liability |
| **Platform operator** | Mainland-registered marketplace (Tmall Global, JD Worldwide, Douyin cross-border) | Must verify **transaction authenticity and consumer identity authenticity**; transmits order data to customs; bears advance-compensation liability to consumers |
| **Domestic service provider** | Mainland-registered entity providing declaration, payment, logistics or warehousing | Transmits payment/logistics/warehousing data to customs and accepts follow-up supervision |
| **Consumer (ordering person)** | The mainland buyer | Taxpayer for the cross-border order; annual personal allowance is tied to their identity |

Two consequences follow that matter for data governance:

1. **The overseas brand is not "outside the system."** It is a named, responsible participant — it just discharges part of that responsibility through a mainland-registered entrustee.
2. **Identity authenticity is a legal duty on the platform**, not merely a commercial fraud check. 486号文 expressly requires platforms to monitor abnormal trading such as repeated bulk orders by the same purchaser, payment account, delivery address or phone number, and **ordering under a misappropriated identity**.

<div class="statcard"><span class="n">100k / 1m / 10k</span><span class="l">China's three-tier personal information export thresholds for a processor that is not a critical information infrastructure operator, counted cumulatively from 1 January of the current year: under 100,000 individuals (non-sensitive) = exempt; 100,000 to under 1,000,000 (or under 10,000 sensitive) = standard contract or certification required; 1,000,000 or more, or 10,000 or more sensitive = mandatory CAC security assessment</span><span class="src">Source: Provisions on Promoting and Regulating Cross-Border Data Flows (CAC Order No. 16), Arts. 5, 7, 8</span></div>

## Step 3 — Map the four data flows in a cross-border order

Most brands only think about flow 4. All four are in scope.

### Flow 1 — Order, payment and logistics data to customs (mandatory, statutory)

Before a cross-border retail import can be declared, the platform or the overseas seller's mainland agent, the payment company and the logistics company must **each** transmit order, payment and logistics electronic data to customs through the International Trade Single Window or a cross-border e-commerce clearance service platform, and each bears responsibility for **data authenticity** (GACC Announcement No. 194 of 2018, s. III(6)). Overseas cross-border e-commerce enterprises must entrust a mainland agent to register with customs in the agent's locality.

This flow contains the buyer's real name, ID number, phone and delivery address. It is not optional and it is not a "marketing" transfer — it is a statutory filing obligation.

### Flow 2 — Buyer identity verification

Customs separately verifies the ordering person's identity. The consumer confirms the transaction in the "掌上海关" (Customs on Hand) or "掌上单一窗口" (Single Window on Hand) mini-program or app by entering name and ID number and passing **face recognition**. The stated legal basis is the Customs Law, GACC Announcement No. 194 of 2018 and the 486号文 notice, and the stated purpose is to prevent identity and annual allowance misappropriation and smuggling through the cross-border channel.

> Practical rule for brands: **do not build your own copy of this.** Face recognition data is biometric information and falls within the sensitive personal information category in PIPL Art. 28, which triggers separate consent and a stricter necessity test. Leave the biometric step to the customs channel.

### Flow 3 — Order fulfilment data back to the overseas brand

This is the flow that crosses the border: the brand's HQ or ERP receives the order, the buyer's name, phone, address, SKU and payment reference so it can pick, pack, invoice and provide after-sales service.

### Flow 4 — CRM, analytics, retargeting and KOL attribution

The highest-risk flow, and the one least likely to qualify for any exemption. Exporting a Chinese buyer profile for global CRM, lookalike audiences, influencer attribution or AI model training has no contract-necessity justification and is counted against the thresholds in Step 4.

## Step 4 — Choose your export gateway (or establish you qualify for the exemption)

PIPL Article 38 requires a processor providing personal information outside China to satisfy one of four conditions: pass a CAC-organised security assessment, obtain personal information protection certification from a professional body, conclude the CAC standard contract with the overseas recipient, or meet other conditions set by law or the regulator.

Since 22 March 2024, CAC Order No. 16 has reorganised which gateway applies — and Order No. 16 Article 13 states that where the earlier measures are inconsistent, **Order No. 16 governs**.

| Cumulative exports since 1 Jan (non-CIIO processor) | Gateway required |
|---|---|
| Contract-necessity transfers (incl. cross-border shopping), **necessary** for a contract with the individual | **Exempt** from all three (Art. 5(1)) |
| Under 100,000 individuals, non-sensitive | **Exempt** (Art. 5(4)) |
| Data collected abroad, processed in China, re-exported **without adding** any China-sourced personal information or important data | **Exempt** (Art. 4) |
| International trade / transport / marketing data containing **no** personal information and no important data | **Exempt** (Art. 3) |
| Within a free trade zone, data **outside** the zone's published negative list | **Exempt** (Art. 6) |
| 100,000 – under 1,000,000 individuals, or under 10,000 sensitive | **Standard contract** *or* **certification** (Art. 8) |
| 1,000,000+ individuals, or 10,000+ sensitive | **CAC security assessment** (Art. 7) |
| Any important data, or any volume if you are a CIIO | **CAC security assessment** (Art. 7) |

### The exemption most cross-border sellers can actually use

Order No. 16 Article 5(1) exempts transfers that are necessary to conclude or perform a contract to which the individual is a party, and the text names **跨境购物 (cross-border shopping)** expressly, alongside cross-border remittance, cross-border payment, ticketing and visa services.

CAC clarified the scope in its October 2025 policy Q&A: the list is **open-ended** ("等" is not exhaustive), but the exemption only holds if **both** conditions are met — (1) the transfer is for concluding or performing a contract to which the individual is a party, and (2) the transfer is genuinely **necessary**, judged against applicable laws, regulations, national standards and the actual export scenario for the minimum necessary scope. The Q&A gave a useful counter-example: a hotel exporting the personal information of a Chinese resident booking a hotel **inside** China does not qualify.

> What this means in practice: the order fulfilment flow (Flow 3) is generally exempt. The CRM and retargeting flow (Flow 4) is not. Run them through separate legal bases and separate systems.

<div class="statcard"><span class="n">10 working days / 3 years</span><span class="l">If you use the standard contract route, you must file the contract and the personal information protection impact assessment report with the provincial cyberspace administration within 10 working days of the contract taking effect — and both the assessment report and the processing records must be retained for at least 3 years. An assessment result, once granted, is valid for 3 years and can be extended by a further 3 years on application made at least 60 working days before expiry</span><span class="src">Source: Measures for the Standard Contract for Outbound Personal Information (CAC Order No. 13), Art. 7; PIPL Art. 56; CAC Order No. 16, Art. 9</span></div>

## Step 5 — The obligations that survive every exemption

This is where most compliance programmes fail. Exemption from the *gateway* is not exemption from the *duties*:

- **Article 10 of Order No. 16** — a processor providing personal information overseas must still perform **notification**, obtain the individual's **separate consent**, and conduct a **personal information protection impact assessment (PIPIA)** under PIPL.
- **PIPL Art. 39** — before exporting, you must tell the individual the overseas recipient's name and contact details, the purpose and method of processing, the categories of personal information, and how the individual can exercise their rights against the overseas recipient — and obtain **separate consent**.
- **PIPL Art. 55(4)** — exporting personal information is a listed trigger for a **pre-transfer** PIPIA. Art. 56 requires the assessment to cover legality/lawfulness, the impact on individual rights and security risk, and whether the protective measures are lawful, effective and proportionate.
- **PIPL Art. 38, final paragraph** — you must take necessary measures to ensure the overseas recipient's processing meets PIPL standards.
- **Network Data Security Management Regulation (State Council Order No. 790, in force 1 January 2025), Art. 21** — your personal information processing rules must be **concentrated, publicly displayed, easily accessible and placed in a prominent position**, and must cover the processor's identity and contact details, purposes/methods/categories, retention period and how the individual exercises rights. Where you collect and onward-provide information, the recipients must be **listed in a manifest**.
- **Same Regulation, Art. 22** — sensitive personal information (biometric, religious belief, specific identity, medical health, financial account, location tracking, and information of children under 14) requires **separate consent**; children under 14 require parental or guardian consent and a dedicated processing rule.

## Step 6 — Appoint a China-side representative and file it

If PIPL Article 3(2) catches you, **Article 53** requires you to either establish a dedicated body in China or **designate a representative** responsible for personal information protection, and to file that body's name or the representative's name and contact details with the competent authority.

The Network Data Security Management Regulation Article 26 pins down the filing channel: the report goes to the **cyberspace administration at the level of the city divided into districts** where the body or representative is located, and that department notifies the relevant competent authorities at the same level.

For a foreign brand running a 1210 test with no mainland entity, the practical solution is to make the designated representative function part of the mainland entrustee relationship you already need under 486号文 — the same mainland-registered enterprise that registers with customs and accepts supervision. Do not leave this as an unassigned legal duty sitting with an overseas entity nobody in China can reach.

## Step 7 — Free trade zone negative lists (a real, under-used lever)

Order No. 16 Article 6 lets a free trade zone publish its own **negative list** of data that stays inside the assessment / standard contract / certification regime. **Data outside the list flows freely** — no assessment, no contract, no certification.

**Tianjin was first.** On 9 May 2024 the Tianjin FTZ Administrative Committee and the Tianjin Commerce Bureau published the *China (Tianjin) Pilot Free Trade Zone Data Export Management List (Negative List) (2024 Edition)* — the first such list approved by a provincial cyberspace committee and filed with the national cyberspace and data authorities after Order No. 16 took effect. It covers **13 broad categories and 46 sub-categories** across eight priority sectors including biomedicine, service outsourcing, finance, internet platforms, automotive, integrated circuits, meteorology and international trade, describing each data category's characteristics with concrete examples. Data outside the list may be exported freely; state secrets, core data and government data are excluded from the list regime and follow their own rules.

<div class="statcard"><span class="n">13 / 46</span><span class="l">The Tianjin Pilot Free Trade Zone data-export negative list classifies outbound data into 13 broad categories and 46 sub-categories across eight priority sectors. For an enterprise inside the zone, anything not on the list may be exported without a security assessment, standard contract or certification — the list is a clearance tool, not just a restriction</span><span class="src">Source: China (Tianjin) Pilot FTZ Data Export Management List (Negative List) (2024 Edition), published 9 May 2024</span></div>

> Why this matters commercially: routing your China data operations through a Tianjin FTZ entity can convert an uncertain "do we need to file?" question into a documented checklist exercise. It is one of the few places where China's data regime gives a foreign-invested business a *published* answer rather than a judgement call.

## Step 8 — What changed in 2024–2026 (and what changed on 1 January 2026)

China's data regime moved fast. Five changes matter for a cross-border seller:

| Instrument | Effective | What changed for you |
|---|---|---|
| **Provisions on Promoting and Regulating Cross-Border Data Flows** (CAC Order No. 16) | 22 Mar 2024 | Raised thresholds, created the exemptions (incl. cross-border shopping), extended assessment validity to 3 years, created FTZ negative lists; overrides earlier measures where inconsistent |
| **Network Data Security Management Regulation** (State Council Order No. 790) | 1 Jan 2025 | Consolidated network data duties; Arts. 21–22 on transparency and consent; Art. 26 filing channel for the Art. 53 representative; Art. 35 restates the eight export gateways |
| **Measures for Personal Information Protection Compliance Audit** (CAC Order No. 18) | 1 May 2025 | A processor handling **more than 10 million individuals'** personal information must conduct a compliance audit **at least once every two years**; regulators may compel an audit after a breach affecting 1 million+ individuals or 100,000+ sensitive records |
| **Measures for Personal Information Export Certification** (CAC + SAMR Order No. 20) | 1 Jan 2026 | Gives the certification route a dedicated procedure: available to non-CIIO processors exporting 100,000–1,000,000 individuals (non-sensitive) or under 10,000 sensitive; a PIPIA with separate consent still required first; splitting volumes to dodge assessment is prohibited |
| **Cybersecurity Law (as amended)** | 1 Jan 2026 | Adds Art. 42(2): network operators processing personal information must comply with the Cybersecurity Law, the Civil Code and PIPL. Raises penalty ceilings for failing security protection duties — RMB 500,000–2 million where the breach causes mass data loss or partial loss of CII function, RMB 2–10 million for particularly serious consequences |

Note the direction of travel: the **gateways** have been loosened repeatedly since 2024, while the **accountability, transparency and audit** obligations have been tightened. Planning on the assumption that "China relaxed data export" is a mistake — what was relaxed is the filing burden, not the liability.

## The eight-step runbook

1. **Confirm PIPL scope.** If you sell to individuals in China, Art. 3(2) applies. Record the conclusion.
2. **Draw a data map** of all four flows, with field-level detail, recipient, purpose and destination. Most brands discover flows they did not know existed.
3. **Sort each flow into a legal basis.** Order fulfilment → Art. 5(1) contract necessity. CRM/marketing → count it, or stop exporting it.
4. **Count the volume** cumulatively from 1 January of the current year, sensitive and non-sensitive separately. Establish which tier you are in — and re-check at 80% of the threshold.
5. **Fix the front end.** Publish a compliant processing rule (Art. 21 of Order 790), add recipient manifests, and build a **separate consent** flow for exports with the Art. 39 disclosures.
6. **Run the PIPIA before** any export starts, and retain the report and records for at least 3 years.
7. **Appoint and file the representative** under PIPL Art. 53 / Order 790 Art. 26. If you use the standard contract, file within 10 working days of it taking effect.
8. **Decide where the data physically sits.** If you operate in a free trade zone, check the negative list before assuming you need to file.

## Where GOODSINFINITE fits

Data compliance in cross-border e-commerce is not a policy document — it is an operating question about who in China is answerable, and what the physical flow looks like. Our structure covers both layers:

- **Hong Kong importer of record** — GOODSINFINITE TRADE LIMITED (Kwun Tong, Kowloon) as your trading counterparty, overseas shipper and FX settlement layer, so the title and payment flow stay outside the mainland data perimeter where they belong.
- **Mainland clearance and compliance** — a licensed China-side operation handles customs registration, declaration and product registration, and can carry the documentation burden that accompanies the statutory data filings.
- **Five-city bonded fulfilment** — Tianjin, Shanghai, Ningbo, Guangzhou, Qingdao. Tianjin gives you access to the FTZ data export negative list regime described above.
- **China-side commercial presence** — office setup, recruitment, market research, trade-show participation and B2B channel building (including 1688.com), plus representation in offline negotiations with Chinese buyers.

<div class="statcard"><span class="n">6,000㎡ + 8,000㎡</span><span class="l">Bonded warehousing and temperature- and humidity-controlled warehousing operated through our network, alongside 300+ enterprises served and our own AEO advanced certification plus 15 partner AEO facilities — the physical layer that determines where your order, payment and logistics data is generated, who transmits it to customs, and how quickly a quarantine or recall hold can be executed</span><span class="src">Source: GOODSINFINITE operations</span></div>

## What we deliberately do not assert

We have kept this article to rules we can point to in official text. Three things are commonly claimed in vendor content that we will not repeat without a source:

- **We do not give a fee or timeline for a CAC security assessment.** No official schedule is published and third-party figures vary widely.
- **We do not state that a Chinese ID number is "sensitive personal information."** PIPL Article 28 lists categories; whether a specific field falls in one is an assessment to be made against Art. 28, not an assumption. Biometric data used in the customs face-recognition step *is* within the listed categories.
- **We do not describe any specific enforcement case or fine against a named company** that we cannot source to an official publication.

## FAQ

**Does PIPL apply to me if I have no Chinese entity?** Yes. PIPL Art. 3(2) captures processing of Chinese residents' personal information from outside China where the purpose is providing products or services to them. Cross-border e-commerce selling is squarely within that.

**Do I need a data export security assessment?** Usually not. The cross-border-shopping contract-necessity exemption (CAC Order No. 16, Art. 5(1)) and the under-100,000-individuals exemption cover most brands. Assessment is mandatory above 1 million individuals or 10,000 sensitive records, or for any important data.

**What data goes to Chinese customs?** Order, payment and logistics electronic data, transmitted separately by the platform/agent, the payment company and the logistics company through the Single Window, each responsible for authenticity. Buyer name and ID number are part of that flow, with a separate buyer identity verification done by the consumer in the customs app.

**Do I need a China-based representative?** If PIPL Art. 3(2) applies to you, yes — Art. 53 requires a dedicated body or designated representative in China, filed with the competent authority (Order 790 Art. 26 specifies the municipal-level cyberspace administration).

**If my export is exempt, is there anything left to do?** Yes. Notification, separate consent and a pre-transfer PIPIA still apply under Order No. 16 Art. 10 and PIPL Arts. 39, 55 and 56.

**What are the penalties?** Up to RMB 1 million for an uncorrected violation; for serious cases RMB 50 million or 5% of the previous year's turnover, business suspension and licence revocation, with RMB 100,000–1,000,000 on responsible individuals and a possible management bar.

## Sources

- [Personal Information Protection Law of the PRC — full text (Arts. 3, 38, 39, 53, 55, 56, 66)](http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html) — National People's Congress
- [Network Data Security Management Regulation (State Council Order No. 790, in force 1 January 2025) — Arts. 21, 22, 26, 27, 35](https://www.gov.cn/gongbao/2024/issue_11646/202410/content_6980863.html) — State Council Gazette
- [Provisions on Promoting and Regulating Cross-Border Data Flows (CAC Order No. 16, 22 March 2024) — Arts. 3–10 in full](https://www.gov.cn/gongbao/2024/issue_11366/202405/content_6954192.html) — State Council Gazette
- [Measures for the Standard Contract for Outbound Personal Information (CAC Order No. 13, in force 1 June 2023) — Art. 7 filing within 10 working days](https://www.gov.cn/gongbao/content/2023/content_5752224.htm) — State Council Gazette
- [Measures for Personal Information Export Certification (CAC and SAMR Order No. 20, published 14 October 2025, in force 1 January 2026) — Art. 5 eligibility](https://www.gov.cn/gongbao/2025/issue_12426/202511/content_7049740.html) — State Council Gazette
- [Measures for Personal Information Protection Compliance Audit (CAC Order No. 18, in force 1 May 2025) — Art. 4: over 10 million individuals, audit at least every two years (official Q&A)](https://www.gov.cn/zhengce/202502/content_7003769.htm) — Cyberspace Administration of China / gov.cn
- [Decision of the NPC Standing Committee on Amending the Cybersecurity Law (adopted 28 October 2025, in force 1 January 2026) — new Art. 42(2), revised Art. 61 penalties](http://www.npc.gov.cn/npc/c1773/c1848/c21114/wlaqfxz/wlaqfxz002/202511/t20251103_449242.html) — National People's Congress
- [Notice on Improving the Supervision of Cross-Border E-Commerce Retail Imports (商财发〔2018〕486号) — four participants, identity authenticity duty, joint and several civil liability](https://cws.mofcom.gov.cn/swcjzc/art/2019/art_399cd4ef63e7401a853f6c00ba391247.html) — MOFCOM / NDRC / MOF / GACC / STA / SAMR
- [GACC Announcement No. 194 of 2018 on Matters Concerning the Supervision of Cross-Border E-Commerce Retail Import and Export Goods — three-document data transmission and data authenticity responsibility](http://www.customs.gov.cn/customs/2018-12/13/article_2025121221010384362.html) — General Administration of Customs
- [Cross-border e-commerce supervision service guide (GACC Announcement No. 194 as the stated legal basis)](https://online.customs.gov.cn/static/pages/guides/000629020000/000629020000.html) — China Customs online service platform
- [State Council Information Office briefing on the post-transition cross-border e-commerce retail import policy — annual allowance raised to RMB 26,000 and single-transaction limit to RMB 5,000](https://www.gov.cn/zhengce/2018-12/08/content_5346963.htm) — gov.cn
- [China (Tianjin) Pilot Free Trade Zone Data Export Management List (Negative List) (2024 Edition) published — 13 categories, 46 sub-categories](https://www.gov.cn/lianbo/difang/202405/content_6950083.htm) — gov.cn / Xinhua

## Related reading

- [What Is 1210 Bonded Import?](https://www.goods-infinite.com/insights/what-is-1210-bonded-import.html)
- [1210 Bonded vs Direct Mail](https://www.goods-infinite.com/insights/1210-bonded-vs-direct-mail.html)
- [Importing Into China Without a Local Company](https://www.goods-infinite.com/insights/importing-into-china-without-a-local-company.html)
- [Hong Kong Entity for China Import](https://www.goods-infinite.com/insights/hong-kong-entity-china-import.html)
- [Tmall Global Store Setup](https://www.goods-infinite.com/insights/tmall-global-store-setup.html)
- [Cross-Border E-Commerce in China](https://www.goods-infinite.com/insights/cross-border-ecommerce-china.html)
- [China Product Recall and SAMR Enforcement](https://www.goods-infinite.com/insights/china-product-recall-samr-enforcement.html)
- [Which Chinese Agency Regulates My Product?](https://www.goods-infinite.com/insights/which-chinese-agency-regulates-my-product.html)
- [China Import Compliance: CCC and NMPA](https://www.goods-infinite.com/insights/china-import-compliance-ccc-nmpa.html)
- [China Social Media Advertising Compliance](https://www.goods-infinite.com/insights/china-social-media-advertising-compliance.html)
- [China Market Entry Guide](https://www.goods-infinite.com/guide-china-market-entry.html)
