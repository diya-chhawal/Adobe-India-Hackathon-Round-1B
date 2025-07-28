# 🧠 Adobe India Hackathon 2025 — Round 1B: Persona-Based PDF Summarization

## 📌 Problem Statement

You are given a batch of PDFs and a task-persona input (`challenge1b_input.json`). The objective is to extract and refine the most relevant information from these documents based on the persona’s job-to-be-done, and output a structured JSON summary.

## 🛠️ Approach

We designed a lightweight NLP-based pipeline optimized for CPU and time-constrained environments. Here's how our system works:

1. **Text Extraction**: We use [PyMuPDF](https://pymupdf.readthedocs.io/) to extract text from PDF pages efficiently.
2. **Section Detection**: Headings and content blocks are identified using regex-based heuristics.
3. **Tokenization & Stemming**: Text is tokenized and stemmed using [NLTK](https://www.nltk.org/), with stopword removal.
4. **TF-IDF Scoring**: Sections are ranked based on term relevance to the job description using a TF-IDF-inspired scheme.
5. **Refinement**: Top-ranked sections are truncated and cleaned to produce high-quality, concise outputs under length constraints.

The output JSON contains:
- `metadata`: Input documents, persona, task, timestamp
- `extracted_sections`: Top 5–10 ranked headings
- `subsection_analysis`: Refined textual summaries

## 📁 Directory Structure
round1b/
├── app/
│ ├── processor.py # Core logic for extraction and ranking
│ └── main.py # Entry point
├── input/ # Contains challenge1b_input.json + PDFs
├── output/ # Output folder for result.json
├── Dockerfile # Containerized execution
├── .gitignore # Ignore pycache and output files
└── README.md # This file


## 📦 Dependencies

The container installs all required packages:

- Python 3.10+
- PyMuPDF
- NLTK (with punkt & stopwords corpora)

No external models or internet access required at runtime.

---

## 🐳 How to Build and Run the Solution

> Make sure Docker is installed and running.

### 🧱 Build the Docker image:

```bash
docker build -t mysolution:round1b .

