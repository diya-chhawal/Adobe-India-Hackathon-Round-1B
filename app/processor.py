import json
import sys
import os
import time
import re
from datetime import datetime
from typing import List, Dict, Any
import math
import argparse
from collections import defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:
    os.system("pip install PyMuPDF")
    import fitz

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer
except ImportError:
    os.system("pip install nltk")
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

class DocumentProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        doc = fitz.open(pdf_path)
        pages_text = {page_num + 1: doc.load_page(page_num).get_text() for page_num in range(len(doc))}
        doc.close()
        return pages_text

    def identify_sections(self, text: str, page_num: int) -> List[Dict[str, Any]]:
        sections = []
        lines = text.split('\n')
        current_section = {'title': '', 'content': '', 'start_line': 0}
        header_patterns = [
            r'^[A-Z][A-Z\s]{2,}$',
            r'^\d+\.?\s+[A-Z].*',
            r'^[A-Z][^.!?]*$',
            r'^\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)\s*$',
        ]

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            is_header = any(re.match(pat, line) and 3 < len(line) < 100 for pat in header_patterns)
            if is_header and current_section['content'].strip():
                sections.append({
                    'title': current_section['title'] or f"Section {len(sections) + 1}",
                    'content': current_section['content'].strip(),
                    'page_number': page_num,
                    'start_line': current_section['start_line']
                })
                current_section = {'title': line, 'content': '', 'start_line': i}
            elif is_header:
                current_section['title'] = line
                current_section['start_line'] = i
            else:
                current_section['content'] += line + ' '

        if current_section['content'].strip():
            sections.append({
                'title': current_section['title'] or f"Section {len(sections) + 1}",
                'content': current_section['content'].strip(),
                'page_number': page_num,
                'start_line': current_section['start_line']
            })
        return sections

    def calculate_tf_idf(self, documents: List[List[str]], query_terms: List[str]) -> List[float]:
        total_docs = len(documents)
        df = defaultdict(int)
        for doc in documents:
            unique = set(doc)
            for term in query_terms:
                if term in unique:
                    df[term] += 1
        scores = []
        for doc in documents:
            doc_score = 0
            doc_len = len(doc) or 1
            term_counts = defaultdict(int)
            for word in doc:
                term_counts[word] += 1
            for term in query_terms:
                tf = term_counts[term] / doc_len
                idf = math.log((total_docs + 1) / (df[term] + 1)) + 1
                doc_score += tf * idf
            scores.append(doc_score)
        return scores

    def calculate_importance_score(self, section, persona, job_description, all_sections):
        score = 0
        content = section['content'].lower()
        title = section['title'].lower()
        tokens = [self.stemmer.stem(t) for t in word_tokenize(content) if t.isalnum() and t not in self.stop_words]
        title_tokens = [self.stemmer.stem(t) for t in word_tokenize(title) if t.isalnum()]
        section['tokens'] = tokens
        query_terms = [self.stemmer.stem(t) for t in word_tokenize(job_description.lower()) if t.isalnum() and t not in self.stop_words]
        all_docs = [s.get('tokens', []) for s in all_sections]
        tfidf_scores = self.calculate_tf_idf(all_docs, query_terms)
        idx = all_sections.index(section)
        if idx < len(tfidf_scores):
            score += tfidf_scores[idx] * 10
        score += sum(5 for kw in query_terms if kw in title_tokens)
        score += sum(2 for kw in query_terms if kw in tokens)
        if 100 <= len(section['content']) <= 2000:
            score += 2
        if 2 <= len(title.split()) <= 12:
            score += 1
        return max(0, score)

    def rank_sections(self, all_sections, persona, job_description, max_sections=10):
        for section in all_sections:
            section['importance_score'] = self.calculate_importance_score(section, persona, job_description, all_sections)
        ranked = sorted(all_sections, key=lambda x: x['importance_score'], reverse=True)
        doc_counter = defaultdict(int)
        top_sections = []
        for sec in ranked:
            doc = sec['document']
            if doc_counter[doc] < 2:
                top_sections.append(sec)
                doc_counter[doc] += 1
            if len(top_sections) == max_sections:
                break
        for i, section in enumerate(top_sections):
            section['importance_rank'] = i + 1
        return top_sections

    def refine_text(self, content, max_length=1000):
        content = re.sub(r'\s+', ' ', content.strip())
        content = re.sub(r'\b\d+\b(?=\s*$)', '', content, flags=re.MULTILINE)
        if len(content) > max_length:
            sentences = sent_tokenize(content)
            refined = ""
            for sentence in sentences:
                if len(refined) + len(sentence) <= max_length:
                    refined += sentence + " "
                else:
                    break
            content = refined.strip()
        return content

    def process_documents(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()

        if 'metadata' in input_data:
            input_documents = input_data['metadata'].get('input_documents', [])
            persona_input = input_data['metadata'].get('persona', '')
            job_to_be_done = input_data['metadata'].get('job_to_be_done', '')
        elif 'documents' in input_data and 'persona' in input_data and 'job_to_be_done' in input_data:
            input_documents = [d['filename'] for d in input_data['documents']]
            persona_input = input_data['persona'].get('role', '')
            job_to_be_done = input_data['job_to_be_done'].get('task', '')
        else:
            raise ValueError("Invalid input format.")

        persona = persona_input.lower()
        documents = [{"filename": f, "title": os.path.splitext(f)[0]} for f in input_documents]

        all_sections = []
        document_names = [doc["filename"] for doc in documents]

        for doc_info in documents:
            filename = doc_info["filename"]
            if not os.path.exists(filename) or not filename.lower().endswith(".pdf"):
                continue
            pages_text = self.extract_text_from_pdf(filename)
            for page_num, text in pages_text.items():
                for section in self.identify_sections(text, page_num):
                    section['document'] = filename
                    all_sections.append(section)

        if not all_sections:
            return {
                "metadata": {
                    "input_documents": [os.path.basename(f) for f in document_names],
                    "persona": persona_input,
                    "job_to_be_done": job_to_be_done,
                    "processing_timestamp": datetime.now().isoformat(),
                    "processing_time_seconds": round(time.time() - start_time, 2)
                },
                "extracted_sections": [],
                "subsection_analysis": []
            }

        top_sections = self.rank_sections(all_sections, persona, job_to_be_done)

        extracted = [{
            "document": os.path.basename(s["document"]),
            "section_title": s["title"],
            "importance_rank": s["importance_rank"],
            "page_number": s["page_number"]
        } for s in top_sections]

        analysis = [{
            "document": os.path.basename(s["document"]),
            "section_title": s["title"],
            "refined_text": self.refine_text(s["content"]),
            "importance_rank": s["importance_rank"],
            "page_number": s["page_number"]
        } for s in top_sections]

        return {
            "metadata": {
                "input_documents": [os.path.basename(f) for f in document_names],
                "persona": persona_input,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp": datetime.now().isoformat(),
                "processing_time_seconds": round(time.time() - start_time, 2)
            },
            "extracted_sections": extracted,
            "subsection_analysis": analysis
        }