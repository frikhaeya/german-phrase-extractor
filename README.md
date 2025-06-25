# 🇩🇪 Gmail German Phrase Extractor

This project extracts German learning content from your Gmail inbox and saves it to a clean, structured CSV file.

It’s tailored for language learners who subscribe to email lessons (like Manuel's verb-focused mini-lessons) and want to organize the material for review, Anki flashcards, or archiving.

---

## ✅ What it Does

- Connects to your Gmail account securely using OAuth 2.0
- Searches for emails labeled `German` and sent by `manuel@herrprofessor.com`
- Extracts:
  - 📌 Phrase in German
  - 🌍 English translation (prefers natural translation, falls back to literal if needed)
  - 🔧 Verb taught in that lesson
  - 📋 Literal translation as example
  - 📨 Subject and 📅 Date of the email (for context)

All results are saved into a file: `german_phrases.csv`

---

## 🧰 Requirements

- Python 3.7+
- Gmail account
- Access to Google Cloud Console

### 📦 Install dependencies

```bash
pip install -r requirements.txt

