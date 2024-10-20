from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, pipeline
from datasets import load_dataset

def fine_tune_llm(data_path="code_quality_dataset.json", model_name="gpt2", output_dir="./code_quality_model"):
    """Fine-tunes an LLM for code smell detection."""

    # Load the dataset using the datasets library
    data = load_dataset('json', data_files=data_path)['train']
    print("Dataset loaded. Columns:", data.column_names)

    # Check if 'code' column exists
    if 'code' not in data.column_names:
        raise KeyError("Expected 'code' column in dataset but not found.")

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # Add a new padding token
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.resize_token_embeddings(len(tokenizer))  # Update embeddings

    # Preprocess data
    def preprocess_function(examples):
        """Tokenizes each code snippet and prepares labels."""
        inputs = tokenizer(examples['code'], padding="max_length", truncation=True, return_tensors="pt")
        inputs['labels'] = inputs['input_ids'].clone()  # Set labels
        return inputs

    print("Tokenizing data...")
    tokenized_data = data.map(preprocess_function, batched=True)  # Use map with batched=True
    print("Data tokenization complete.")

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=2,  # Reduce batch size for testing
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
    )

    # Start training
    print("Starting training...")
    trainer.train()
    print("Training complete.")

    # Save the model
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)  # Save the tokenizer as well
    print("Model and tokenizer saved.")

    print("Fine-tuning complete.")
