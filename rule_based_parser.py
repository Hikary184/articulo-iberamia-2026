"""
Rule-Based Pre-segmentation Parser
Stage 1 of the Hybrid AI Pipeline for Lexicographic Knowledge Extraction

This script performs deterministic pre-processing on raw dictionary text files.
It normalizes OCR artifacts, standardizes whitespaces, segments the text into
individual lexical entries, and extracts explicit structural boundaries 
(e.g., Headword, Part of Speech) using regular expressions and heuristics.
The output is an intermediate JSON format ready for LLM semantic completion.
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

def normalize_text(raw_text: str) -> str:
    """
    Normalizes character encoding, removes non-printable symbols,
    standardizes whitespace, and corrects common OCR artifacts.
    """
    # Standardize whitespaces and newlines
    text = re.sub(r'[ \t]+', ' ', raw_text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    # Correct common OCR artifacts (e.g., rn -> m, l -> 1 in specific contexts)
    # Note: These are basic examples; specific OCR rules vary by dictionary format.
    text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    
    return text.strip()

def segment_entries(text: str) -> List[str]:
    """
    Segments the full dictionary document into individual lexical entries.
    Assumes entries are separated by double newlines or follow a specific 
    typographic pattern (e.g., start with a bold marker or specific indentation).
    """
    # Simple heuristic: split by double newline. 
    # Can be adjusted to match regex like r'\n(?=[A-ZÁÉÍÓÚÑ])' depending on the source.
    raw_entries = re.split(r'\n{2,}', text)
    return [entry.strip() for entry in raw_entries if len(entry.strip()) > 2]

def extract_deterministic_fields(raw_entry: str) -> Dict[str, Any]:
    """
    Extracts explicit lexical fields using handcrafted regular expressions.
    Maps the extracted data to the foundational structure of the target schema.
    """
    # Initialize the base schema (partially filled)
    structured_entry = {
        "entry": raw_entry,
        "lemma": "",
        "part_of_speech": [],
        "senses": [],
        "raw_text": raw_entry # Preserved for the LLM prompt
    }
    
    # 1. Extract Headword (Lemma)
    # Heuristic: The first word(s) before a comma, dot, or bracket.
    lemma_match = re.match(r'^([^\.,\(\[0-9]+)', raw_entry)
    if lemma_match:
        structured_entry["lemma"] = lemma_match.group(1).strip()
    
    # 2. Extract Part of Speech (POS)
    # Heuristic: Look for standard grammatical abbreviations in italics or brackets.
    # Examples: (s.), (v.), adj., v.tr., n.
    pos_pattern = re.compile(r'\b(s\.|v\.|adj\.|adv\.|v\.tr\.|v\.intr\.|n\.|pron\.)\b')
    pos_matches = pos_pattern.findall(raw_entry)
    if pos_matches:
        # Clean the punctuation for the schema
        structured_entry["part_of_speech"] = [pos.replace('.', '') for pos in pos_matches]
    
    # 3. Pre-segment Definitions and Examples (Basic split)
    # The LLM will perform the deep semantic structuring of this part.
    # We just create an empty skeleton.
    structured_entry["senses"].append({
        "definition": "",
        "examples": []
    })
    
    return structured_entry

def process_dictionary_file(input_path: Path, output_path: Path):
    """
    Reads a raw text file, processes all entries, and exports the intermediate JSON.
    """
    print(f"Processing raw file: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    normalized_text = normalize_text(raw_text)
    raw_entries = segment_entries(normalized_text)
    
    print(f"Segmented {len(raw_entries)} potential entries. Extracting deterministic fields...")
    
    processed_entries = []
    for entry in raw_entries:
        parsed_data = extract_deterministic_fields(entry)
        processed_entries.append(parsed_data)
        
    # Export intermediate structured data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_entries, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully exported intermediate data to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Deterministic Rule-Based Pre-segmentation Parser")
    parser.add_argument("--input", type=str, required=True, help="Directory containing raw TXT dictionaries")
    parser.add_argument("--output", type=str, required=True, help="Directory to save intermediate JSON files")
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist.")
        return
        
    # Process all text files in the input directory
    for txt_file in input_dir.glob("*.txt"):
        output_file = output_dir / f"{txt_file.stem}_interim.json"
        process_dictionary_file(txt_file, output_file)

if __name__ == "__main__":
    main()