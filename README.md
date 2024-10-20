# Code Smell Detection with Fine-Tuned GPT-2

This project uses a fine-tuned GPT-2 model to detect code smells in Python code. The model is trained to analyze code snippets and suggest potential improvements or highlight issues.

## Project Overview

The goal of this project is to create a tool that assists in detecting code smells in Python code. We fine-tuned the GPT-2 model on a custom dataset of code snippets, enabling the model to generate predictions based on code structure and content.

## Features

- Fine-tuned GPT-2 model for code smell detection.
- Supports input Python code snippets and provides feedback on possible issues.
- Pipeline-based inference for easy usage of the fine-tuned model.

## Technologies Used

- Python for building the scripts.
- Hugging Face's Transformers for model fine-tuning and generation.
- Datasets for loading and preparing the dataset.
  nltk for text processing.
- Virtual Environment for isolated dependency management.

## Setup Instructions

**1. Clone the Repository**

```bash
git clone https://github.com/your-username/code-smell-detector.git
cd code-smell-detector
```

**2. Set Up Virtual Environment**

Make sure you have **virtualenv** installed, then create and activate your virtual environment:

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv .env

# Activate the virtual environment
# On Windows
.env\Scripts\activate
# On macOS/Linux
source .env/bin/activate
```

**3. Install Dependencies**

Install the required packages using pip and the requirements.txt file:

```bash
pip install -r requirements.txt
```

**4. Download NLTK Resources**

Download the NLTK resources that are used in the project:

```bash
import nltk
nltk.download('punkt')
```

**5. Fine-Tune the Model**

To fine-tune the model on your dataset, run:

```bash
python analyzer.py
```

This will load your dataset, fine-tune the GPT-2 model, and save the model to the <code>code_quality_model</code> directory.

**6. Test the Model**

To test the fine-tuned model, run:

```bash
python test_model.py
```

This script will run the model on predefined Python code snippets and display the generated predictions.

**7. Structure of the Project**

- <code>analyzer.py</code>: Fine-tunes the GPT-2 model on the provided dataset for code smell detection.
- <code>fine_tune_llm.py</code>: Code for tuning the model, written separately
- <code>test_model.py</code>: Tests the fine-tuned model with sample Python code snippets.
- <code>code_quality_dataset</code>.json: Sample dataset used for training.
- <code>code_quality_model/</code>: Directory where the fine-tuned model is saved.
- <code>requirements.txt</code>: List of required packages for the project.

## Docker Setup

[Docker Hub](https://hub.docker.com/r/annany/red-string-assignment)

**Dependencies**

The project requires the following packages, which are listed in <code>requirements.txt </code>:

- <code> transformers </code>
- <code> torch </code>
- <code> datasets </code>
- <code> nltk </code>
- <code> virtualenv </code>
- <code> ast </code>
- <code> subprocess </code>
- <code> math </code>
