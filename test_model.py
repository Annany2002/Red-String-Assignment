from transformers import pipeline

def load_model(model_path):
    """Load the fine-tuned model and tokenizer."""
    return pipeline("text-generation", model=model_path)

def clean_output(text):
    """Removes unnecessary characters and trims spaces."""
    return text.replace('\xa0', ' ').strip()

def test_code_snippets(code_smell_detector, snippets):
    """Test the model with a list of code snippets and return cleaned results."""
    results = []
    for snippet in snippets:
        # Generate prediction with controlled randomness
        prediction = code_smell_detector(
            snippet, 
            max_length=50, 
            num_return_sequences=1, 
            truncation=True,
            temperature=0.7,  # Less randomness
            top_k=50          # Only select from top 50 tokens
        )
        
        # Clean the generated text
        cleaned_prediction = clean_output(prediction[0]['generated_text'])
        
        # Append original and predicted code
        results.append({"code": snippet, "prediction": cleaned_prediction})
    return results

def main():
    # Load the fine-tuned model
    model_path = "./code_quality_model"
    code_smell_detector = load_model(model_path)

    # Define some code snippets to test
    test_snippets = [
        "def long_function(a, b, c):\n    # some code\n    return a + b + c",
        "class User:\n    def __init__(self, name):\n        self.name = name",
        "def my_long_function(a, b, c, d, e, f):\n    return a + b + c + d + e + f",
        "class Admin(User):\n    def __init__(self, name, role):\n        super().__init__(name)\n        self.role = role"
    ]

    # Test the snippets and get cleaned results
    results = test_code_snippets(code_smell_detector, test_snippets)

    # Print the results
    for result in results:
        print(f"Code Snippet:\n{result['code']}\nPrediction:\n{result['prediction']}\n{'-'*50}")

if __name__ == "__main__":
    main()
