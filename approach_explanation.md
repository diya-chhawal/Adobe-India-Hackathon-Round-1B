```markdown
# Approach Explanation - Round 1B

## 🎯 Objective

Given:
- A JSON input defining persona + task + list of PDFs
- A set of PDF documents

We must extract the **most relevant sections** across all documents, and return:
1. `extracted_sections` ranked by importance
2. `subsection_analysis` with refined summaries

---

## 🧠 Strategy

### 1. **Text Extraction**
- Uses **PyMuPDF** (`fitz`) to extract text page-by-page.
- Each page's lines are scanned for possible **headers** using regex.

### 2. **Section Identification**
- Sections are split using heuristics:
  - Fully capitalized lines
  - Numbered headings (e.g. `1. Introduction`)
  - Title-case lines with no sentence punctuation
- Sections store:
  - Title, content, page number, and start line.

### 3. **Relevance Scoring**
Each section is scored using:
- **TF-IDF matching** between section and job description
- Token overlap with job keywords
- Title significance boost
- Length and formatting heuristics

### 4. **Ranking & Filtering**
- Top 10 sections selected across all docs
- At most 2 per document to ensure diversity
- Ranked by total relevance score

### 5. **Refinement**
- Trims/refines each section's content using `nltk.sent_tokenize`
- Limits to ~1000 characters
- Removes excess whitespace and isolated numbers

---

## 🧪 NLP & Heuristics

- Uses `nltk` for:
  - Tokenization
  - Stopword removal
  - Sentence splitting
  - Stemming with `PorterStemmer`

---

## ⚙️ Output

Follows the challenge spec:
- Includes metadata (files, persona, job, timestamp)
- Contains 2 main arrays:
  - `extracted_sections`
  - `subsection_analysis` (with `refined_text`)

---

## 🚫 Assumptions & Limitations

- Relies on formatting heuristics — may miss sections in poorly formatted PDFs.
- Does not use external LLMs or embeddings (per Docker constraint).
- Assumes input JSON is well-formed and PDFs are OCR-readable.

---

## 🛠 Technologies Used

| Tool        | Purpose             |
|-------------|---------------------|
| Python 3    | Language             |
| PyMuPDF     | PDF Parsing          |
| NLTK        | NLP & Summarization  |
| Docker      | Isolated Execution   |

---

## 🏁 Result

Efficient, lightweight, and deterministic processor that runs inside Docker and returns concise, task-aligned JSON summaries across multiple PDFs.
```