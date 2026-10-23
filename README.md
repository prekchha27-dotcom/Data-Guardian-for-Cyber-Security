# 🛡️ Data Guardian — Social Media Privacy & Legal Policy Research Dashboard

**Author:** Prekchha Thakur  
**Type:** Educational Prototype — Python / Streamlit  
**Deployment:** Local (`localhost`) or Streamlit Community Cloud

---

## Project Description

**Data Guardian** is a fully self-contained, interactive Streamlit dashboard that helps everyday users understand the privacy practices, legal terms, and cybersecurity risks of nine major social media and digital platforms.

It was built as an educational tool — there is no real device access, no live data scraping, and no API keys required. Everything runs locally on your machine.

### What it does

| Section | Purpose |
|---|---|
| 📤 Upload Latest Privacy Policy | Browse 9 platforms × 6 policy categories, open official documents, paste policy text, and generate a plain-English extractive summary |
| 📱 App Privacy Library | Browse detailed app profiles: permissions, data sharing, security risks, and recommended actions |
| 🔍 Permission Explorer | Learn what every device permission means, what data it exposes, and what risk level it carries |
| 🌐 Third-Party Data Access | Understand who else receives your data (advertisers, SDKs, OAuth apps) and explore interactive data-flow diagrams |
| ✅ Review My Access | Step-by-step action centre to review device permissions, revoke connected apps, and track your privacy review progress |
| 🎓 Cybersecurity Learning Centre | Plain-language explanations of 12 cybersecurity concepts + 3 documented real-world case studies |

---

## Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.9+ | Core language |
| Streamlit | ≥ 1.32.0 | Web dashboard framework (frontend + backend) |
| Standard Library (`re`, `math`, `heapq`, `collections`, `textwrap`) | Built-in | Local extractive summarizer — no API needed |

> **Note:** The entire application — UI layout, navigation, data, and summarization logic — is written in Python using Streamlit. There is no separate frontend or backend server.

---

## Accessibility

The colour palette was designed to be accessible for low-vision users:

- Minimum contrast ratio **4.5 : 1** for all body text (WCAG AA compliant)
- Base font size **17px**, line-height **1.7**
- All focus states show a **3px teal outline** for keyboard navigation
- Colour is never the only way information is conveyed (icons + labels are always paired)
- Status badges and alert boxes all carry sufficient contrast on their backgrounds

---

## Platforms Covered

WhatsApp · Instagram · Facebook · Telegram · Snapchat · Flipkart · Google · Gmail · GitHub

## Policy Categories Covered

Privacy Policy · Terms of Service · Community Guidelines & Acceptable Use · Third-Party Material & Services · Limitation of Liability · Arbitration & Legal Dispute Waivers

---

## Setup & Run Instructions

### Requirements

- Python 3.9 or later  
- pip (comes with Python)

### Step 1 — Install dependencies (one time only)

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 2 — Start the dashboard

```bash
streamlit run data_guardian_app.py
```

### Step 3 — Open the dashboard in your browser

Streamlit prints a URL like:

```
Local URL:   http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Open the **Local URL** in your browser.

---

## How to Use the Summarize Policy Feature

1. Click **Upload Latest Privacy Policy** in the left sidebar.
2. Select a **platform** (e.g. WhatsApp) and a **policy category** (e.g. Privacy Policy).
3. Select your **region** (India / United States / Global).
4. Click the official link shown to open the real policy document in a new tab.
5. Select all text on that page (**Ctrl+A** / **Cmd+A**) and copy it.
6. Paste the text into the **Paste Policy Text** box.
7. Click **Summarize Policy**.
8. The plain-English summary appears immediately below.

### How the summarizer works

- Built entirely from Python's standard library — **no AI service, no internet, no API key**.
- Splits pasted text into sentences, scores each sentence by word frequency (TF-IDF-inspired), and selects the highest-scoring sentences under category-specific headings.
- This is an **extractive** summary — it copies real sentences from your pasted document. It does not rewrite or interpret them.
- **Not legal advice.**

---

## Deploying Online (for your teacher or examiner)

The easiest free option is **Streamlit Community Cloud**:

1. Push this project to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app → choose your repo → set Main file path to `data_guardian_app.py`**.
4. Click **Deploy**. You will receive a permanent public URL in ~2 minutes.

---

## Project Structure

```
data_guardian_app.py                          ← single-file app (all code combined)
requirements.txt                              ← Python dependencies (streamlit only)
README.md                                     ← this file
PrekchhaThakur_ProjectReport_WithScreenshots.docx  ← project report
sections/                                     ← original modular source files (reference)
  styles.py · data.py · policy_data.py
  upload_policy.py · app_library.py
  permission_explorer.py · third_party.py
  review_access.py · learning_centre.py
  summarizer.py · policy_hub.py
```

> **Deployment note:** `data_guardian_app.py` is fully self-contained.
> It does not import from the `sections/` folder — all code is inlined.
> Only `data_guardian_app.py` and `requirements.txt` are needed to run the app.

---

## Key Limitations

- The summarizer selects existing sentences — it does not generate new explanations.
- Policy links are verified as of June 2025. Always check the official platform website for the current document.
- Data Guardian cannot access, read, or modify device permissions — it is a web application.
- All app data is demonstration material for educational purposes. Nothing here is legal advice.

---

## Upgrading to AI Summarization (Optional)

If you later want AI-powered summaries via OpenAI:

```bash
pip install openai
# Windows:
set DG_OPENAI_API_KEY=sk-...
# Mac/Linux:
export DG_OPENAI_API_KEY=sk-...
streamlit run data_guardian_app.py
```

The summarizer in `sections/summarizer.py` is designed to be swapped — the rest of the dashboard does not need to change.
