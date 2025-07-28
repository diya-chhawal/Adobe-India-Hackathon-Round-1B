# Approach Explanation

This solution uses rule-based section extraction and TF-IDF + persona keyword scoring to identify relevant sections.

Key steps:
1. Extract text from PDFs using PyMuPDF
2. Identify headers using regex-based heuristics
3. Score each section by:
   - TF-IDF relevance to job description
   - Persona keyword match (primary/secondary)
   - Heuristics (length, numeric presence, etc.)
4. Return top-ranked sections in the expected JSON format

No internet access or external models are required.