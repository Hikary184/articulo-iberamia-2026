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

```

⚙️ Hardware & Software Requirements
Due to the size of the chosen model (Qwen2.5-72B-Instruct), inference requires specific hardware capabilities and offloading strategies. The experiments in the paper were executed using the following setup:

CPU: Intel Core i7-14700F

System RAM: 64 GB DDR5 (Required for CPU offloading)

GPU: NVIDIA GeForce RTX 4060 Ti (16 GB VRAM)

OS: Windows 11 Pro / Ubuntu 22.04 LTS

Inference Precision: 4-bit quantization (GPTQ/AWQ)

🚀 Installation
Clone the repository:

Bash
git clone [https://github.com/your-username/lexicographic-hybrid-ai.git](https://github.com/your-username/lexicographic-hybrid-ai.git)
cd lexicographic-hybrid-ai
Create and activate a virtual environment (Python 3.11 recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install PyTorch with CUDA support (crucial for GPU acceleration). Visit PyTorch's official site to get the correct command for your CUDA version. Example for CUDA 12.1:

Bash
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
Install the remaining project dependencies:

Bash
pip install -r requirements.txt
🧠 Usage
1. Rule-Based Pre-segmentation
Run the deterministic parser to identify explicit structural boundaries and generate intermediate partially-structured data:

Bash
python src/rule_based_parser.py --input data/raw/ --output data/interim/
2. LLM Semantic Completion
Execute the inference script to process the intermediate data. This script enforces a Temperature = 0.0 and Greedy Decoding for deterministic reproducibility:

Bash
python src/llm_inference.py --input data/interim/ --output data/processed/ --schema schema/target_schema.json
3. Evaluation
Calculate extraction metrics (Precision, Recall, F1-Score, Missing Field Rate) against the Gold Standard dataset:

Bash
python src/evaluate_metrics.py --predictions data/processed/ --ground_truth data/gold_standard_350.json
📊 Dataset Notice
The data/gold_standard_350.json file contains a manually annotated subset of 350 entries used for the empirical evaluation (70 entries per dictionary). Due to copyright and intellectual property restrictions from the original publishers (INAH, INALI, etc.), the full corpora of 16,300 entries are not publicly distributed in this repository.

🤝 Acknowledgments
This study was supported by the Organización de Estados Iberoamericanos para la Educación, la Ciencia y la Cultura (OEI) under grant number OEI/FC25-26/006/MULT
