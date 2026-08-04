# articulo-iberamia-2026

# Hybrid AI for Lexicographic Knowledge Extraction 📖🤖

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official repository for the paper: **"Hybrid AI for Lexicographic Knowledge Extraction: Transforming Dictionaries into Structured Lexical Databases"**.

This project implements a sequential hybrid artificial intelligence pipeline that combines deterministic rule-based parsing with Large Language Model (LLM) semantic completion to digitize printed Indigenous language dictionaries into machine-readable JSON formats.

## 📌 Abstract / Overview
The digitization of historical and low-resource language dictionaries poses a complex information extraction challenge due to typographical heterogeneity, implicit semantic boundaries, and orthographic variations. This project introduces a hybrid pipeline that mitigates the brittleness of traditional parsers and the hallucination risks of standalone LLMs. 

The pipeline uses **Qwen2.5-72B-Instruct** for constrained semantic completion over a pre-segmented structural backbone. The methodology was evaluated on a multilingual corpus of 16,300 entries from five Latin American Indigenous languages (Yalalag Zapotec, Sierra Popoluca, Iskonawa, Modern Nahuatl, and Yucatec Maya).

## 📂 Repository Structure

```text
lexicographic-hybrid-ai/
├── README.md                  # Project documentation and usage instructions
├── requirements.txt           # Python dependencies
│
├── data/
│   └── gold_standard_350.json # Subset of 350 manually annotated entries for evaluation
│
├── prompts/
│   ├── system_prompt.txt      # System instructions and behavior rules for Qwen2.5
│   └── user_prompt.txt        # Template for raw dictionary entry ingestion
│
├── schema/
│   └── target_schema.json     # Relational JSON schema constraints
│
└── src/
    ├── rule_based_parser.py   # Deterministic pre-segmentation using regular expressions
    ├── llm_inference.py       # LLM inference script (4-bit quantization, CPU-GPU offloading)
    └── evaluate_metrics.py    # Script for calculating F1-Score, Precision, Recall, and IAA
