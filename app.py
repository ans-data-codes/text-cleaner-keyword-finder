"""
Text Cleaner & Keyword Finder
-----------------------------
A simple, beginner-friendly Streamlit web application that cleans text,
calculates key statistics, searches for keywords, and visualizes word frequencies.

Tech Stack:
- Python 3
- Streamlit (Web interface)
- re (Regular Expressions for cleaning and search)
- collections.Counter (Word frequency analysis)
- pandas (Data organization for the frequency bar chart)
"""

import re
from collections import Counter
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Text Cleaner & Keyword Finder",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Optional custom CSS for styling metrics and visual polish
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
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. Text Processing Functions
# -----------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Cleans the input text in three straightforward steps:
    1. Lowercase: Converts all characters to lowercase for uniformity.
    2. Remove Punctuation: Replaces non-alphanumeric characters and underscores with a space.
    3. Normalize Whitespace: Replaces multiple spaces, tabs, or newlines with a single space.
    """
    if not text:
        return ""
    
    # Step 1: Convert text to lowercase
    lowered = text.lower()
    
    # Step 2: Remove punctuation and symbols (replace with space to prevent glued words)
    no_punctuation = re.sub(r"[^\w\s]|_", " ", lowered)
    
    # Step 3: Normalize whitespace (collapse multiple spaces/tabs/newlines and strip edges)
    normalized = re.sub(r"\s+", " ", no_punctuation).strip()
    
    return normalized


def calculate_metrics(text: str):
    """
    Computes total words, total characters, and unique words count.
    """
    if not text or not text.strip():
        return 0, 0, 0
    words = text.split()
    total_words = len(words)
    total_characters = len(text)
    unique_words = len(set(words))
    return total_words, total_characters, unique_words


def search_keyword(text: str, keyword: str, whole_word: bool = False) -> int:
    """
    Counts case-insensitive occurrences of a word or phrase in text.
    Uses re.escape to safely handle any regex characters inside the keyword.
    """
    if not text or not keyword or not keyword.strip():
        return 0
    
    escaped_keyword = re.escape(keyword.strip())
    
    if whole_word:
        # \b ensures word boundaries so 'cat' will not match 'catalog'
        pattern = rf"\b{escaped_keyword}\b"
    else:
        # Substring / phrase match
        pattern = escaped_keyword
        
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)


def get_top_frequent_words(cleaned_text: str, top_n: int = 10):
    """
    Extracts the top N most frequent words using collections.Counter.
    """
    if not cleaned_text or not cleaned_text.strip():
        return []
    words = cleaned_text.split()
    counter = Counter(words)
    return counter.most_common(top_n)


# -----------------------------------------------------------------------------
# 3. Session State Management
# -----------------------------------------------------------------------------
SAMPLE_TEXT = (
    "Streamlit is an open-source Python framework for building web applications! "
    "With Streamlit, data scientists and developers can quickly create clean, interactive, "
    "and responsive data tools. Text processing in Python often uses regular expressions (the re module) "
    "and collections.Counter. For example, text cleaner tools remove punctuation, normalize whitespace, "
    "and convert text to lowercase. Regular expressions make keyword searching fast and case-insensitive. "
    "Streamlit makes data visualization simple with built-in bar charts, charts, and metrics."
)

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "cleaned_output" not in st.session_state:
    st.session_state["cleaned_output"] = ""
if "has_cleaned" not in st.session_state:
    st.session_state["has_cleaned"] = False


# -----------------------------------------------------------------------------
# 4. Sidebar: Guide & Viva Cheatsheet
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("📘 About This App")
    st.write(
        "A beginner-friendly text analytics tool designed for college viva demonstrations "
        "and everyday text preprocessing."
    )
    
    st.markdown("---")
    st.subheader("💡 Viva Cheatsheet")
    with st.expander("1. Text Cleaning with `re`", expanded=False):
        st.code(
            '# Lowercase\ntext = text.lower()\n\n'
            '# Remove punctuation\ntext = re.sub(r"[^\\w\\s]|_", " ", text)\n\n'
            '# Normalize whitespace\ntext = re.sub(r"\\s+", " ", text).strip()',
            language="python",
        )
        st.caption("Converts to lowercase, removes punctuation/symbols, and collapses whitespace.")

    with st.expander("2. Frequency with `Counter`", expanded=False):
        st.code(
            "from collections import Counter\n"
            "words = cleaned_text.split()\n"
            "counts = Counter(words)\n"
            "top_10 = counts.most_common(10)",
            language="python",
        )
        st.caption("Splits text into words and returns the 10 most common words.")

    with st.expander("3. Keyword Finder with `re`", expanded=False):
        st.code(
            'matches = re.findall(\n'
            '    re.escape(keyword),\n'
            '    text,\n'
            '    flags=re.IGNORECASE\n'
            ')\n'
            'count = len(matches)',
            language="python",
        )
        st.caption("Uses `re.escape()` to safely handle special symbols and `re.IGNORECASE`.")

    st.markdown("---")
    st.caption("🚀 Built with Python, Streamlit, `re`, and `collections.Counter`.")


# -----------------------------------------------------------------------------
# 5. Main Application Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">📝 Text Cleaner & Keyword Finder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Clean unstructured text, compute word statistics, search keywords, '
    'and visualize word frequency distributions.</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 6. Input Section
# -----------------------------------------------------------------------------
st.subheader("1. Enter or Paste Text")

# Action bar with helper buttons
col_act1, col_act2, col_act3 = st.columns([1.5, 1.5, 5])
with col_act1:
    if st.button("📋 Load Sample Text", help="Load an example text snippet for testing"):
        st.session_state["user_input"] = SAMPLE_TEXT
        st.session_state["cleaned_output"] = clean_text(SAMPLE_TEXT)
        st.session_state["has_cleaned"] = True
        st.rerun()

with col_act2:
    if st.button("🗑️ Clear Text", help="Clear the input text area"):
        st.session_state["user_input"] = ""
        st.session_state["cleaned_output"] = ""
        st.session_state["has_cleaned"] = False
        st.rerun()

# Text Area input
raw_input = st.text_area(
    label="Type or paste your text below:",
    value=st.session_state["user_input"],
    height=160,
    placeholder="Paste a paragraph, essay, article, or any raw text here...",
    key="text_input_area",
)

# Keep session state synchronized with user typing
if raw_input != st.session_state["user_input"]:
    st.session_state["user_input"] = raw_input

# Clean Text button
clean_col, _ = st.columns([2, 6])
with clean_col:
    clean_clicked = st.button("🧹 Clean Text", type="primary", use_container_width=True)

if clean_clicked:
    if not raw_input.strip():
        st.warning("⚠️ Please enter or paste some text before clicking **Clean Text**.")
        st.session_state["has_cleaned"] = False
    else:
        st.session_state["cleaned_output"] = clean_text(raw_input)
        st.session_state["has_cleaned"] = True
        st.success("✅ Text cleaned successfully! Punctuation removed, converted to lowercase, and whitespace normalized.")

# Display Cleaned Text Output
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

# -----------------------------------------------------------------------------
# 7. Text Statistics Section
# -----------------------------------------------------------------------------
st.subheader("2. Text Statistics")

# Allow the user to select which version to analyze
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

# Calculate metrics
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

# -----------------------------------------------------------------------------
# 8. Keyword Search Section
# -----------------------------------------------------------------------------
st.subheader("3. Keyword Search")
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
        help="If checked, searching 'cat' will match 'cat' but not 'cathedral'.",
    )

if keyword_query.strip():
    if not active_text.strip():
        st.warning("⚠️ Please provide text in the input area above to search for keywords.")
    else:
        occurrences = search_keyword(active_text, keyword_query, whole_word=match_whole)
        if occurrences > 0:
            st.success(
                f'🎯 Found **{occurrences}** case-insensitive occurrence(s) of **"{keyword_query.strip()}"** '
                f'in the {"cleaned" if st.session_state["has_cleaned"] else "input"} text.'
            )
        else:
            st.warning(
                f'🔍 No occurrences of **"{keyword_query.strip()}"** were found in the text.'
            )
else:
    st.caption("Type a word or phrase above to see its total occurrences.")

st.markdown("---")

# -----------------------------------------------------------------------------
# 9. Top 10 Most Frequent Words Bar Chart
# -----------------------------------------------------------------------------
st.subheader("4. Word Frequency Analysis (Top 10 Words)")

# For word frequency, cleaned text is always preferred so punctuation is not counted as part of a word
freq_source = (
    st.session_state["cleaned_output"]
    if (st.session_state["has_cleaned"] and st.session_state["cleaned_output"])
    else clean_text(raw_input)
)

top_words = get_top_frequent_words(freq_source, top_n=10)

if not top_words:
    st.info("📊 Enter or clean some text above to view the top 10 most frequent words bar chart.")
else:
    # Build a DataFrame for Streamlit bar chart
    df_top_words = pd.DataFrame(top_words, columns=["Word", "Frequency"])
    
    chart_col, table_col = st.columns([3, 2])
    with chart_col:
        st.write("##### 📊 Top 10 Word Frequencies")
        chart_data = df_top_words.set_index("Word")
        st.bar_chart(chart_data, y="Frequency")
    
    with table_col:
        st.write("##### 📋 Frequency Breakdown")
        st.dataframe(
            df_top_words,
            hide_index=True,
            use_container_width=True,
        )

# -----------------------------------------------------------------------------
# 10. Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Text Cleaner & Keyword Finder • Built with Python & Streamlit • "
    "Designed for College Project Demonstrations & Vivas."
)
