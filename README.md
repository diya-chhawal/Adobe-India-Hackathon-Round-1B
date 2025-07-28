# Adobe India Hackathon - Round 1B Submission

This repository contains my solution for **Round 1B** of the Adobe India Hackathon. The task involves processing a set of input PDF documents and generating a consolidated structured JSON output, based on the given persona and job-to-be-done.

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

  - **`README.md`**: Contains instructions on how to build, run, and test the solution.

  - **`approach_explanation.md`**: Explains the methodology used — document processing, ranking strategy, relevance logic, etc.

---

## 🧪 How to Build and Run

### 🔧 Build the Docker Image
```bash
docker build --platform linux/amd64 -t mysolution:round1b .
