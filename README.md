# 📘 Adobe India Hackathon — Round 1B Solution

This repository contains a Dockerized solution for Round 1B of the Adobe India Hackathon. The objective of this challenge is to generate a single structured JSON output from a batch of PDF documents based on a user's persona and job-to-be-done. The output includes the most relevant sections and refined summaries that best satisfy the user's intent.

---

## 🔍 Problem Overview

Given:
- A set of related PDF documents
- A structured input JSON defining the user's role and task

The task is to:
- Parse and analyze all PDFs
- Identify and rank the most relevant sections
- Generate concise summaries of those sections
- Output all information in a single JSON file with metadata

---

## 🧠 Approach Summary

1. **Text Extraction**:  
   PDFs are parsed using PyMuPDF (`fitz`). The solution processes each page, extracts raw text, and breaks it into candidate sections based on formatting patterns (e.g., all caps, numbered headers, or bold-like cues).

2. **Section Detection**:  
   Using regex-based heuristics, text blocks are grouped into coherent sections, each tagged with a title, page number, and content.

3. **Relevance Scoring**:  
   Each section is scored for relevance using a TF-IDF-based method. The job description from the input JSON is preprocessed, tokenized, and stemmed. Sections are ranked based on term frequency and overlap with query tokens.

4. **Heuristic Enhancements**:  
   Relevance is further enhanced with rule-based scoring for:
   - Title-query overlap
   - Section length
   - Title clarity

5. **Ranking & Filtering**:  
   To ensure document diversity, at most 2 sections are picked per PDF. The top 10 most relevant sections across all documents are retained and ranked.

6. **Subsection Refinement**:  
   Each selected section is cleaned and summarized, maintaining sentence boundaries and fitting within a ~1000 character limit.

7. **Output**:  
   The result is written to a single JSON file with:
   - Metadata (input files, timestamps, persona, etc.)
   - Ranked sections with titles and page numbers
   - Refined summaries

---

## 📁 Directory Structure (Explained)

- **`round1b/`**: Root directory of the project.

  - **`app/`**: Contains core Python logic.
    - `processor.py`: Main module for PDF parsing, section extraction, ranking, and scoring.
    - `main.py`: Entry point that reads input JSON and calls the processor to generate output.

  - **`input/`**: Folder with all input files.
    - `challenge1b_input.json`: Input metadata file (job description, persona, and PDF references).
    - `*.pdf`: Set of input PDF documents.

  - **`output/`**: Stores the generated `result.json` after processing.

  - **`Dockerfile`**: Defines the container image, environment setup, and how to run the code inside Docker.

  - **`README.md`**: Contains instructions on how to build, run, and test the solution. Explains the methodology used — document processing, ranking strategy, relevance logic, etc.

---

## 🧪 How to Build and Run

### 🔧 Build the Docker Image
```bash
docker build --platform linux/amd64 -t mysolution:round1b .

### Execute Processing
```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none mysolution:round1b python3 processor.py /app/input/challenge1b_input.json /app/output/result.json



