import os
import logging
from pdfminer.high_level import extract_text as pdf_extract_text
import docx2txt
from sentence_transformers import SentenceTransformer
import torch
import re
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)


def smart_chunk(text):
    pattern = r'^(Name|Skills|Technical Skills|Education|Experience|Projects|Certifications|Languages|Summary|Profile|Contact|About):?'
    lines = text.split('\n')

    chunks = []
    current_section = "Header"
    buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        heading_match = re.match(pattern, line, re.IGNORECASE)
        if heading_match:
            if buffer:
                chunks.append(f"{current_section}: {' '.join(buffer)}")
                buffer = []
            current_section = heading_match.group(1).capitalize()
        else:
            buffer.append(line)

    if buffer:
        chunks.append(f"{current_section}: {' '.join(buffer)}")

    return list(set(chunks))


# Lazy load model
_model = None

def get_model():
    global _model
    if _model is None:
        logging.info("Loading SentenceTransformer model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


# Global cache for CV embeddings
embeddings_cache = {}


def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    try:
        file_extension = file_extension.lower()
        if file_extension == '.pdf':
            return pdf_extract_text(file_path)
        elif file_extension in ['.docx', '.doc']:
            return docx2txt.process(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        logging.error(f"Error extracting text from file: {str(e)}")
        return ""


def create_embeddings(text):
    chunks = smart_chunk(text)
    if not chunks:
        return None, []

    model = get_model()
    embeddings = model.encode(chunks, convert_to_tensor=True)
    return embeddings, chunks


def update_embeddings(cvs):
    global embeddings_cache
    embeddings_cache.clear()

    for cv in cvs:
        if cv.extracted_text:
            embeddings, chunks = create_embeddings(cv.extracted_text)
            if embeddings is not None:
                embeddings_cache[cv.id] = {
                    'embeddings': embeddings,
                    'chunks': chunks
                }


boost_keywords = {
    "name": ["name", "who are you", "your name"],
    "skills": ["skills", "technologies", "tools", "stack"],
    "education": ["school", "college", "university", "degree", "graduation"],
    "experience": ["experience", "worked", "employed", "job", "role"],
    "projects": ["projects", "built", "developed", "created"],
    "contact": ["email", "phone", "linkedin", "github", "contact"]
}


def get_label_score_boost(label, question):
    question = question.lower()
    for key, words in boost_keywords.items():
        if key in label:
            for word in words:
                if word in question:
                    return 0.3
    return 0.0


def format_chunk(label, content, max_sentences=2):
    label = label.capitalize()
    # Clean and split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', content.strip())
    short_content = ' '.join(sentences[:max_sentences])
    
    # Special case for Skills: comma-separate and limit to ~5 items
    if label == "Skills":
        skills = list(set(re.split(r'[\n,;\-\u2022]+', content)))
        skills = [s.strip() for s in skills if s.strip()]
        short_content = ', '.join(skills[:5])

    return f"{label}: {short_content}"


def answer_question(question, max_chunks=3):
    if not embeddings_cache:
        return "No CVs are currently loaded."

    model = get_model()
    q_embedding = model.encode([question], convert_to_tensor=True)

    results = []
    seen_chunks = set()

    for cv_data in embeddings_cache.values():
        embeddings = cv_data['embeddings']
        chunks = cv_data['chunks']

        similarities = torch.nn.functional.cosine_similarity(q_embedding, embeddings)

        for score, chunk in zip(similarities, chunks):
            if ':' in chunk:
                label, content = chunk.split(':', 1)
                label = label.lower()
                boost = get_label_score_boost(label, question)
                adjusted_score = score.item() + boost

                if adjusted_score > 0.25 and chunk not in seen_chunks:
                    formatted = format_chunk(label, content)
                    results.append((adjusted_score, formatted))
                    seen_chunks.add(chunk)

    if not results:
        return "No relevant information found."

    results.sort(key=lambda x: x[0], reverse=True)
    top_chunks = results[:max_chunks]

    response = "\n".join([chunk for _, chunk in top_chunks])
    return response.strip()

