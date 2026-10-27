# Text Cleaner & Keyword Finder

A simple, beginner-friendly web application built with **Python** and **Streamlit** for cleaning raw text, calculating text statistics, searching for keywords, and visualizing word frequencies.

---

## 📌 Project Overview

When dealing with unstructured text (such as articles, user reviews, or essays), raw text often contains unwanted punctuation, inconsistent casing, and irregular whitespace. 

This application provides an intuitive graphical interface to:
1. Preprocess and clean text in three clear, standardized steps.
2. Calculate key text metrics (word count, character count, and unique word count).
3. Search for specific words or phrases (case-insensitive).
4. Visualize the top 10 most frequent words in a bar chart.

Everything runs locally or in the cloud without requiring databases, external APIs, API keys, or machine-learning models.

---

## ✨ Features

- **Text Input & Sample Loader**: Type or paste any text into an expandable text area. Includes a **Load Sample Text** button for quick testing during demonstrations.
- **Clean Text Transformation**:
  - Converts all characters to **lowercase**.
  - Removes **punctuation and symbols** using regular expressions (`re`).
  - Normalizes **whitespace** by converting multiple spaces, tabs, and newlines into a single space.
- **Real-Time Text Statistics**:
  - 📄 **Total Words**
  - 🔤 **Total Characters**
  - 💎 **Unique Words**
  - Ability to toggle metrics between original and cleaned text.
- **Case-Insensitive Keyword Search**:
  - Searches for any word or multi-word phrase using `re.findall`.
  - Safely handles special regex characters with `re.escape()`.
  - Includes an optional "Match whole words only" toggle.
- **Word Frequency Visualization**:
  - Extracts the top 10 most frequent words using `collections.Counter`.
  - Displays an interactive bar chart and frequency breakdown table using `st.bar_chart` and `pandas`.
- **Graceful Error & Empty State Handling**:
  - Clean warning and info banners if the input is blank or when no matches are found.
  - Zero crashes or uncaught exceptions.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language |
| **Streamlit** | Interactive web user interface |
| **`re` (Standard Library)** | Regular expressions for text cleaning and keyword searching |
| **`collections.Counter` (Standard Library)** | Efficient frequency counting for words |
| **`pandas`** | Structuring tabular data for bar chart visualization |

---

## 📁 Project Structure

```text
text-cleaner-keyword-finder/
├── app.py              # Main Streamlit web application
├── requirements.txt    # Application dependencies (streamlit, pandas)
└── README.md           # Documentation, viva reference, and setup guide
```

---

## 🚀 How to Run Locally

### Prerequisites
Make sure you have **Python 3.9+** installed on your system.

### Step 1: Clone or Navigate to the Project Folder
Open your terminal or PowerShell and navigate to the project root:
```bash
cd path/to/text-cleaner-keyword-finder
```

### Step 2: (Optional) Create and Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```
*(If `streamlit` is not recognized on your path directly, run `python -m streamlit run app.py`).*

### Step 5: Open in Browser
Once started, the app will automatically open in your default browser at:
```
http://localhost:8501
```

---

## ☁️ How to Deploy to Streamlit Community Cloud

Streamlit Community Cloud is a free, zero-configuration hosting platform designed specifically for Streamlit apps.

### Step 1: Push Code to GitHub
Ensure all files are committed and pushed to your GitHub repository:
```bash
git add app.py requirements.txt README.md
git commit -m "feat: complete text cleaner and keyword finder application"
git push origin main
```

### Step 2: Sign In to Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Sign in using your **GitHub account**.

### Step 3: Create a New App
1. Click the **"New app"** button in the dashboard.
2. Select your repository: `ans-data-codes/text-cleaner-keyword-finder`.
3. Select the branch: `main`.
4. Set the Main file path: `app.py`.
5. Click **"Deploy!"**.

### Step 4: Access Your Live App
Streamlit will install the packages from `requirements.txt` and launch the application. You will receive a public URL (e.g., `https://text-cleaner-keyword-finder.streamlit.app/`) that anyone can access.

---

## 🎓 College Viva & Interview Cheatsheet

### 1. How does the text cleaning function work?
Text cleaning is performed in three distinct steps using the built-in `re` module:
```python
# 1. Lowercase
lowered = text.lower()

# 2. Punctuation removal (replaces non-alphanumeric characters with a space)
no_punctuation = re.sub(r"[^\w\s]|_", " ", lowered)

# 3. Whitespace normalization (collapses multiple spaces/newlines into a single space)
normalized = re.sub(r"\s+", " ", no_punctuation).strip()
```
- **Why replace punctuation with a space?** If we simply delete punctuation (e.g. `word1,word2`), the words might get joined together into `word1word2`. Replacing with a space avoids this.
- **Why lowercase?** Text comparisons and counts become uniform and case-insensitive.

### 2. How does word frequency counting work?
We split the cleaned text into a list of words using `.split()`, then pass the list to Python's `collections.Counter`:
```python
from collections import Counter

words = cleaned_text.split()
counter = Counter(words)
top_10 = counter.most_common(10)
```
- `Counter` is a dictionary subclass designed specifically for counting hashable objects.
- `most_common(10)` returns a list of the 10 highest-frequency tuples `(word, count)` ordered by count.

### 3. How does the keyword search work?
Keyword occurrences are found using `re.findall()`:
```python
escaped_keyword = re.escape(keyword.strip())
matches = re.findall(escaped_keyword, text, flags=re.IGNORECASE)
count = len(matches)
```
- `re.escape()` ensures any special regex characters (such as `+`, `?`, `*`, `(`, `)`) in the user's input are treated as literal characters rather than regex operators.
- `re.IGNORECASE` guarantees that uppercase and lowercase occurrences are matched equally.
