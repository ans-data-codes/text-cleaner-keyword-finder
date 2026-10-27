"""
Text Cleaner & Keyword Finder
-----------------------------
A beginner-friendly Streamlit web application that cleans text, computes
statistics, searches keywords, and performs NLP analysis (stop word removal,
stemming, word frequency, and TF-IDF keyword extraction).

Tech Stack:
- Python 3
- Streamlit       — Web interface
- re              — Regex for cleaning and keyword search
- collections.Counter — Word frequency counting
- pandas          — Data organisation for charts
- nltk            — Stop word removal & Porter Stemming
- scikit-learn    — TF-IDF vectorisation
"""

import re
from collections import Counter
import pandas as pd
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK stopwords corpus on first run (silent)
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

# ---------------------------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Text Cleaner & Keyword Finder",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 2. Text Processing Functions
# ---------------------------------------------------------------------------
_stemmer = PorterStemmer()
_stop_words = set(stopwords.words("english"))


def clean_text(text: str, remove_sw: bool = False, apply_stem: bool = False) -> str:
    """
    Cleans input text in up to five steps:
      1. Lowercase
      2. Remove punctuation / symbols (replaced with a space)
      3. Normalize whitespace (collapse spaces/tabs/newlines)
      4. (Optional) Remove English stop words
      5. (Optional) Apply Porter Stemming
    """
    if not text:
        return ""

    # Step 1 — Lowercase
    lowered = text.lower()

    # Step 2 — Remove punctuation & symbols
    no_punct = re.sub(r"[^\w\s]|_", " ", lowered)

    # Step 3 — Normalize whitespace
    normalized = re.sub(r"\s+", " ", no_punct).strip()

    if not (remove_sw or apply_stem):
        return normalized

    # Steps 4 & 5 — Word-level processing (optional)
    words = normalized.split()
    if remove_sw:
        words = [w for w in words if w not in _stop_words]
    if apply_stem:
        words = [_stemmer.stem(w) for w in words]
    return " ".join(words)


def calculate_metrics(text: str):
    """Returns (total_words, total_characters, unique_words)."""
    if not text or not text.strip():
        return 0, 0, 0
    words = text.split()
    return len(words), len(text), len(set(words))


def search_keyword(text: str, keyword: str, whole_word: bool = False) -> int:
    """
    Counts case-insensitive occurrences of a word or phrase in text.
    Uses re.escape() to safely handle special regex characters.
    """
    if not text or not keyword or not keyword.strip():
        return 0
    escaped = re.escape(keyword.strip())
    pattern = rf"\b{escaped}\b" if whole_word else escaped
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def get_top_frequent_words(cleaned_text: str, top_n: int = 10):
    """Top N most frequent words using collections.Counter."""
    if not cleaned_text or not cleaned_text.strip():
        return []
    return Counter(cleaned_text.split()).most_common(top_n)


def get_tfidf_keywords(documents: list, top_n: int = 10):
    """
    Computes mean TF-IDF score for every term across all documents and
    returns the top N as [(term, score), ...].

    TF-IDF (Term Frequency–Inverse Document Frequency) rewards words that
    appear frequently in some documents but rarely across the whole corpus,
    making them more meaningful than raw word counts.
    """
    if not documents or len(documents) < 2:
        return []
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf_matrix = vectorizer.fit_transform(documents)
        mean_scores = tfidf_matrix.mean(axis=0).A1          # average across docs
        feature_names = vectorizer.get_feature_names_out()
        top_indices = mean_scores.argsort()[-top_n:][::-1]  # highest scores first
        return [(feature_names[i], float(mean_scores[i])) for i in top_indices]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# 3. Session State Initialisation
# ---------------------------------------------------------------------------
SAMPLE_TEXT = (
    "Streamlit is an open-source Python framework for building web applications! "
    "With Streamlit, data scientists and developers can quickly create clean, interactive, "
    "and responsive data tools. Text processing in Python often uses regular expressions (the re module) "
    "and collections.Counter. For example, text cleaner tools remove punctuation, normalize whitespace, "
    "and convert text to lowercase. Regular expressions make keyword searching fast and case-insensitive. "
    "Streamlit makes data visualization simple with built-in bar charts, charts, and metrics."
)

for key, default in [
    ("user_input",    ""),
    ("cleaned_output", ""),
    ("has_cleaned",   False),
    ("dataset",       []),    # list of raw document strings loaded from CSV
    ("dataset_name",  ""),    # filename of the uploaded CSV
    ("remove_sw",     False),
    ("apply_stem",    False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------------------------------------------------------------------
# 4. Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("📘 About This App")
    st.write(
        "A beginner-friendly NLP tool for text cleaning, keyword search, "
        "frequency analysis, and TF-IDF keyword extraction from CSV datasets."
    )
    st.markdown("---")
    st.subheader("💡 Viva Cheatsheet")

    with st.expander("1. Text Cleaning (`re`)", expanded=False):
        st.code(
            'text = text.lower()\n'
            'text = re.sub(r"[^\\w\\s]|_", " ", text)\n'
            'text = re.sub(r"\\s+", " ", text).strip()',
            language="python",
        )
        st.caption("Lowercase → remove punctuation → normalize whitespace.")

    with st.expander("2. Stop Word Removal (`nltk`)", expanded=False):
        st.code(
            "from nltk.corpus import stopwords\n"
            "stop = set(stopwords.words('english'))\n"
            "words = [w for w in words if w not in stop]",
            language="python",
        )
        st.caption("Removes common filler words: 'the', 'is', 'a', 'and' …")

    with st.expander("3. Stemming (`nltk`)", expanded=False):
        st.code(
            "from nltk.stem import PorterStemmer\n"
            "ps = PorterStemmer()\n"
            "words = [ps.stem(w) for w in words]\n"
            "# 'running' → 'run',  'happily' → 'happili'",
            language="python",
        )
        st.caption("Reduces words to their root (stem) form.")

    with st.expander("4. Word Frequency (`Counter`)", expanded=False):
        st.code(
            "from collections import Counter\n"
            "counts = Counter(cleaned.split())\n"
            "top_10 = counts.most_common(10)",
            language="python",
        )

    with st.expander("5. TF-IDF (`scikit-learn`)", expanded=False):
        st.code(
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "vec = TfidfVectorizer(stop_words='english')\n"
            "tfidf = vec.fit_transform(documents)\n"
            "# mean score across all docs\n"
            "scores = tfidf.mean(axis=0).A1",
            language="python",
        )
        st.caption("Measures keyword importance across multiple documents.")

    with st.expander("6. Keyword Search (`re`)", expanded=False):
        st.code(
            "matches = re.findall(\n"
            "    re.escape(keyword), text,\n"
            "    flags=re.IGNORECASE\n"
            ")\ncount = len(matches)",
            language="python",
        )

    st.markdown("---")
    st.caption("🚀 Python · Streamlit · re · Counter · nltk · scikit-learn")


# ---------------------------------------------------------------------------
# 5. Main Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="main-title">📝 Text Cleaner & Keyword Finder</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Clean text · compute statistics · search keywords · '
    'extract TF-IDF keywords from CSV datasets.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 6. CSV Dataset Upload  ← NEW SECTION
# ---------------------------------------------------------------------------
st.subheader("1. Upload a CSV Dataset (Optional)")
st.write(
    "Upload a Kaggle CSV (e.g. **SMS Spam Collection** or **News Headlines**) "
    "to analyse 100–200 texts at once. "
    "The dataset drives the **TF-IDF Keyword Analysis** section below. "
    "You can still paste a single text in Section 2."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="Any CSV with a text column works. Kaggle SMS Spam or news headline datasets are ideal.",
    key="csv_uploader",
)

if uploaded_file is not None:
    try:
        df_upload = pd.read_csv(uploaded_file, encoding="latin-1")
        st.success(f"✅ Loaded **{len(df_upload):,} rows** from `{uploaded_file.name}`.")

        # Let user pick the text column
        selected_col = st.selectbox(
            "Select the column containing the text:",
            options=df_upload.columns.tolist(),
            key="text_col_select",
        )

        # Slider to control sample size (10–200)
        max_rows = min(200, len(df_upload))
        sample_size = st.slider(
            "Number of texts to analyse (max 200):",
            min_value=10,
            max_value=max_rows,
            value=max_rows,
            step=10,
        )

        texts = (
            df_upload[selected_col]
            .dropna()
            .astype(str)
            .iloc[:sample_size]
            .tolist()
        )

        with st.expander(f"📄 Preview — first 5 of {len(texts)} texts", expanded=False):
            for i, t in enumerate(texts[:5], 1):
                st.markdown(f"**{i}.** {t}")

        if st.button("✅ Confirm & Load Dataset", type="primary"):
            st.session_state["dataset"]      = texts
            st.session_state["dataset_name"] = uploaded_file.name
            # Also populate the text area with all texts joined (for single-text analysis)
            st.session_state["user_input"]    = "\n".join(texts)
            st.session_state["cleaned_output"] = ""
            st.session_state["has_cleaned"]   = False
            st.success(
                f"🗂️ **{len(texts)} texts** loaded from `{uploaded_file.name}`. "
                "Scroll down to see TF-IDF analysis."
            )
            st.rerun()

    except Exception as exc:
        st.error(f"❌ Could not read the CSV file. Error: {exc}")

elif st.session_state["dataset"]:
    st.info(
        f"🗂️ Active dataset: **{st.session_state['dataset_name']}** "
        f"— {len(st.session_state['dataset'])} texts loaded. "
        "Upload a new CSV to replace it."
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# 7. Text Input  (existing UI — unchanged)
# ---------------------------------------------------------------------------
st.subheader("2. Enter or Paste Text")

col_act1, col_act2, col_act3 = st.columns([1.5, 1.5, 5])
with col_act1:
    if st.button("📋 Load Sample Text", help="Load an example text snippet for testing"):
        st.session_state["user_input"] = SAMPLE_TEXT
        st.session_state["cleaned_output"] = clean_text(
            SAMPLE_TEXT,
            remove_sw=st.session_state["remove_sw"],
            apply_stem=st.session_state["apply_stem"],
        )
        st.session_state["has_cleaned"] = True
        st.rerun()

with col_act2:
    if st.button("🗑️ Clear Text", help="Clear the input text area"):
        st.session_state["user_input"]     = ""
        st.session_state["cleaned_output"] = ""
        st.session_state["has_cleaned"]    = False
        st.rerun()

raw_input = st.text_area(
    label="Type or paste your text below:",
    value=st.session_state["user_input"],
    height=160,
    placeholder="Paste a paragraph, essay, article, or any raw text here...",
    key="text_input_area",
)

if raw_input != st.session_state["user_input"]:
    st.session_state["user_input"] = raw_input

# --- Advanced Cleaning Options (new — collapsible so existing UI is unchanged) ---
with st.expander("⚙️ Advanced Cleaning Options", expanded=False):
    sw_col, stem_col = st.columns(2)
    with sw_col:
        remove_sw = st.checkbox(
            "Remove Stop Words",
            value=st.session_state["remove_sw"],
            help="Removes common English words ('the', 'is', 'a', 'and') that carry little meaning.",
            key="sw_checkbox",
        )
    with stem_col:
        apply_stem = st.checkbox(
            "Apply Stemming (Porter)",
            value=st.session_state["apply_stem"],
            help="Reduces words to their root: 'running' → 'run', 'happily' → 'happili'.",
            key="stem_checkbox",
        )
    st.session_state["remove_sw"]   = remove_sw
    st.session_state["apply_stem"]  = apply_stem

    if remove_sw or apply_stem:
        active_steps = []
        if remove_sw:
            active_steps.append("stop word removal")
        if apply_stem:
            active_steps.append("Porter stemming")
        st.caption(f"ℹ️ Active pipeline additions: {' + '.join(active_steps)}.")

# Clean Text button
clean_col, _ = st.columns([2, 6])
with clean_col:
    clean_clicked = st.button("🧹 Clean Text", type="primary", use_container_width=True)

if clean_clicked:
    if not raw_input.strip():
        st.warning("⚠️ Please enter or paste some text before clicking **Clean Text**.")
        st.session_state["has_cleaned"] = False
    else:
        st.session_state["cleaned_output"] = clean_text(
            raw_input,
            remove_sw=st.session_state["remove_sw"],
            apply_stem=st.session_state["apply_stem"],
        )
        st.session_state["has_cleaned"] = True
        steps = ["lowercase", "punctuation removed", "whitespace normalized"]
        if st.session_state["remove_sw"]:
            steps.append("stop words removed")
        if st.session_state["apply_stem"]:
            steps.append("stemming applied")
        st.success(f"✅ Text cleaned: {', '.join(steps)}.")

# Display cleaned output
if st.session_state["has_cleaned"] and st.session_state["cleaned_output"]:
    st.markdown("#### 🧼 Cleaned Text Output")
    st.text_area(
        label="Cleaned text (lowercase, punctuation removed, single spaces):",
        value=st.session_state["cleaned_output"],
        height=130,
        disabled=False,
        help="You can copy this cleaned text directly.",
        key="cleaned_display",
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# 8. Text Statistics  (existing — unchanged)
# ---------------------------------------------------------------------------
st.subheader("3. Text Statistics")

if st.session_state["has_cleaned"] and st.session_state["cleaned_output"]:
    target_choice = st.radio(
        "Choose text to calculate statistics for:",
        options=["Cleaned Text (Recommended)", "Original Text"],
        horizontal=True,
    )
    active_text = (
        st.session_state["cleaned_output"]
        if target_choice == "Cleaned Text (Recommended)"
        else raw_input
    )
else:
    active_text = raw_input

total_words, total_chars, unique_words = calculate_metrics(active_text)

metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="📄 Word Count", value=f"{total_words:,}")
with metric_col2:
    st.metric(label="🔤 Character Count", value=f"{total_chars:,}")
with metric_col3:
    st.metric(label="💎 Unique Words", value=f"{unique_words:,}")

if not active_text.strip():
    st.info("ℹ️ Enter text above to see word, character, and unique word counts.")

st.markdown("---")

# ---------------------------------------------------------------------------
# 9. Keyword Search  (existing — unchanged)
# ---------------------------------------------------------------------------
st.subheader("4. Keyword Search")
st.write("Find and count occurrences of any word or phrase (case-insensitive).")

search_col1, search_col2 = st.columns([3, 2])
with search_col1:
    keyword_query = st.text_input(
        "Search Keyword or Phrase:",
        placeholder="e.g. streamlit, python, data science",
        key="keyword_input",
    )
with search_col2:
    match_whole = st.checkbox(
        "Match whole words only",
        value=False,
        help="If checked, 'cat' will match 'cat' but not 'cathedral'.",
    )

if keyword_query.strip():
    if not active_text.strip():
        st.warning("⚠️ Please provide text in the input area above to search for keywords.")
    else:
        occurrences = search_keyword(active_text, keyword_query, whole_word=match_whole)
        if occurrences > 0:
            st.success(
                f'🎯 Found **{occurrences}** case-insensitive occurrence(s) of '
                f'**"{keyword_query.strip()}"** in the '
                f'{"cleaned" if st.session_state["has_cleaned"] else "input"} text.'
            )
        else:
            st.warning(f'🔍 No occurrences of **"{keyword_query.strip()}"** found.')
else:
    st.caption("Type a word or phrase above to see its total occurrences.")

st.markdown("---")

# ---------------------------------------------------------------------------
# 10. Word Frequency Bar Chart  (existing — unchanged)
# ---------------------------------------------------------------------------
st.subheader("5. Word Frequency Analysis (Top 10 Words)")

freq_source = (
    st.session_state["cleaned_output"]
    if (st.session_state["has_cleaned"] and st.session_state["cleaned_output"])
    else clean_text(
        raw_input,
        remove_sw=st.session_state["remove_sw"],
        apply_stem=st.session_state["apply_stem"],
    )
)

top_words = get_top_frequent_words(freq_source, top_n=10)

if not top_words:
    st.info("📊 Enter or clean some text above to view the top 10 most frequent words bar chart.")
else:
    df_top_words = pd.DataFrame(top_words, columns=["Word", "Frequency"])

    chart_col, table_col = st.columns([3, 2])
    with chart_col:
        st.write("##### 📊 Top 10 Word Frequencies")
        st.bar_chart(df_top_words.set_index("Word"), y="Frequency")
    with table_col:
        st.write("##### 📋 Frequency Breakdown")
        st.dataframe(df_top_words, hide_index=True, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# 11. TF-IDF Keyword Analysis  ← NEW SECTION
# ---------------------------------------------------------------------------
st.subheader("6. TF-IDF Keyword Analysis")

if not st.session_state["dataset"]:
    st.info(
        "📂 Upload a CSV dataset in **Section 1** above to unlock TF-IDF analysis. "
        "TF-IDF needs multiple documents to compare keyword importance across texts — "
        "a single text is not enough."
    )
else:
    dataset_docs = st.session_state["dataset"]
    st.write(
        f"Analysing **{len(dataset_docs)} documents** from "
        f"`{st.session_state['dataset_name']}`. "
        "Keywords are ranked by their mean TF-IDF score across all documents."
    )

    # Apply the same cleaning settings (stop words / stemming) to each document
    with st.spinner("⏳ Computing TF-IDF scores across all documents…"):
        cleaned_docs = [
            clean_text(
                doc,
                remove_sw=st.session_state["remove_sw"],
                apply_stem=st.session_state["apply_stem"],
            )
            for doc in dataset_docs
        ]
        tfidf_keywords = get_tfidf_keywords(cleaned_docs, top_n=10)

    if not tfidf_keywords:
        st.warning(
            "⚠️ Could not compute TF-IDF scores. "
            "Ensure the dataset has at least 2 non-empty text documents."
        )
    else:
        df_tfidf = pd.DataFrame(tfidf_keywords, columns=["Keyword", "TF-IDF Score"])

        tfidf_chart_col, tfidf_table_col = st.columns([3, 2])
        with tfidf_chart_col:
            st.write("##### 📊 Top 10 TF-IDF Keywords")
            st.bar_chart(df_tfidf.set_index("Keyword"), y="TF-IDF Score")
        with tfidf_table_col:
            st.write("##### 📋 TF-IDF Score Breakdown")
            st.dataframe(
                df_tfidf.style.format({"TF-IDF Score": "{:.4f}"}),
                hide_index=True,
                use_container_width=True,
            )

        st.caption(
            "ℹ️ **TF-IDF** (Term Frequency–Inverse Document Frequency): "
            "a word scores higher when it appears frequently in some documents "
            "but rarely across the whole dataset — capturing more meaningful keywords "
            "than simple word counts."
        )

# ---------------------------------------------------------------------------
# 12. Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Text Cleaner & Keyword Finder • "
    "Built with Python, Streamlit, nltk & scikit-learn • "
    "Designed for College Project Demonstrations & Vivas."
)
