# Text Cleaner & Keyword Finder

A beginner-friendly NLP web application built with **Python** and **Streamlit** that cleans raw text, computes text statistics, searches for keywords, analyses word frequencies, removes stop words, applies stemming, and extracts **TF-IDF keywords** from a Kaggle CSV dataset.

---

## 📌 Project Overview

This app processes unstructured text (news headlines, SMS messages, articles) through a full NLP preprocessing pipeline and provides interactive analytics including frequency charts and TF-IDF keyword rankings — all without any database, external API, or machine-learning model training.

---

## ✨ Features

| # | Feature | Details |
|:--|:--------|:--------|
| 1 | **CSV Dataset Upload** | Upload a Kaggle CSV (e.g. SMS Spam, News Headlines). Select the text column and choose 10–200 rows to analyse. |
| 2 | **Text Cleaning** | Converts to lowercase, removes punctuation and symbols with `re`, normalizes whitespace. |
| 3 | **Stop Word Removal** | Filters out common English filler words ('the', 'is', 'a', 'and') using `nltk.corpus.stopwords`. |
| 4 | **Stemming** | Reduces words to their root form ('running' → 'run') using `nltk.stem.PorterStemmer`. |
| 5 | **Text Statistics** | Displays total words, total characters, and unique word count with toggle between original and cleaned text. |
| 6 | **Keyword Search** | Case-insensitive occurrence count of any word or phrase using `re.findall` and `re.escape`. Includes whole-word matching toggle. |
| 7 | **Word Frequency Bar Chart** | Top 10 most frequent words plotted as a bar chart using `collections.Counter` and `st.bar_chart`. |
| 8 | **TF-IDF Keyword Analysis** | Extracts the top 10 keywords by mean TF-IDF score across all dataset documents using `sklearn.TfidfVectorizer`. |
| 9 | **Graceful Error Handling** | Warning banners for empty inputs, missing datasets, and edge cases — no crashes. |
| 10 | **Viva Cheatsheet Sidebar** | Embedded code snippets explaining every concept in the sidebar. |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|:-----------|:--------|
| **Python 3** | Core programming language |
| **Streamlit** | Interactive web user interface |
| **`re`** (stdlib) | Regex for text cleaning and keyword search |
| **`collections.Counter`** (stdlib) | Word frequency counting |
| **`pandas`** | Data organisation for bar charts |
| **`nltk`** | Stop word removal and Porter Stemming |
| **`scikit-learn`** | TF-IDF vectorisation (`TfidfVectorizer`) |

---

## 📁 Project Structure

```text
text-cleaner-keyword-finder/
├── app.py              # Main Streamlit application (all logic + UI)
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignores pycache, venv, .env files
└── README.md           # Documentation and viva reference
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9 or higher

### Step 1: Navigate to the Project Folder
```bash
cd path/to/text-cleaner-keyword-finder
```

### Step 2: (Optional) Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

> **Note:** On first run, `nltk` will automatically download the English stopwords corpus (~30 KB). No manual download needed.

---

## 📂 Recommended Kaggle Datasets

| Dataset | Link | Suggested Text Column |
|:--------|:-----|:----------------------|
| SMS Spam Collection | [kaggle.com/datasets/uciml/sms-spam-collection-dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) | `v2` (message text) |
| All the News — Headlines | [kaggle.com/datasets/snapcrack/all-the-news](https://www.kaggle.com/datasets/snapcrack/all-the-news) | `title` |
| BBC News Summary | [kaggle.com/datasets/pariza/bbc-news-summary](https://www.kaggle.com/datasets/pariza/bbc-news-summary) | `text` |

---

## ☁️ How to Deploy to Streamlit Community Cloud

1. **Push code to GitHub:**
   ```bash
   git add app.py requirements.txt README.md .gitignore
   git commit -m "feat: add NLP preprocessing and TF-IDF keyword analysis"
   git push origin main
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
   - Click **"New app"** → select your repository → branch: `main` → file: `app.py`.
   - Click **"Deploy!"**.

3. Streamlit Cloud installs `requirements.txt` automatically and provides a public URL.

---

## 🎓 College Viva Reference

### Q1: How is text cleaned?
```python
text = text.lower()                            # Step 1: Lowercase
text = re.sub(r"[^\w\s]|_", " ", text)        # Step 2: Remove punctuation
text = re.sub(r"\s+", " ", text).strip()      # Step 3: Normalize whitespace
```

### Q2: How are stop words removed?
```python
from nltk.corpus import stopwords
stop = set(stopwords.words("english"))
words = [w for w in words if w not in stop]   # Filter filler words
```

### Q3: How does stemming work?
```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()
words = [ps.stem(w) for w in words]           # 'running' → 'run'
```

### Q4: How is word frequency calculated?
```python
from collections import Counter
counts = Counter(cleaned_text.split())
top_10 = counts.most_common(10)               # [(word, count), ...]
```

### Q5: How does TF-IDF work?
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vec   = TfidfVectorizer(stop_words="english")
tfidf = vec.fit_transform(documents)          # sparse matrix
scores = tfidf.mean(axis=0).A1               # mean score per term
# Sort descending to get top keywords
top_indices = scores.argsort()[-10:][::-1]
```
**TF-IDF** (Term Frequency–Inverse Document Frequency) rewards words that appear frequently in some documents but rarely across the whole dataset, making them more meaningful than raw word counts.

### Q6: How does keyword search work?
```python
import re
matches = re.findall(re.escape(keyword), text, flags=re.IGNORECASE)
count = len(matches)     # `re.escape` handles special characters safely
```
