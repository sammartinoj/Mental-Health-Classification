import argparse
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Define label mapping
label_mapping = {
    0: 'Anxiety',
    1: 'Bipolar',
    2: 'Depression',
    3: 'Normal',
    4: 'Personality-disorder',
    5: 'Stress',
    6: 'Suicidal'
}

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Interactive Text Classification with Hugging Face Models")
    parser.add_argument(
        "--model", 
        type=str, 
        required=True 
    )
    parser.add_argument(
        "--text", 
        type=str, 
        required=True
    )

    args = parser.parse_args()

    # Load model and tokenizer
    model_name = args.model
    text = args.text

    print(f"Loading model: {model_name}")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract logits and compute probabilities
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # Get the predicted class and its label
    predicted_class = logits.argmax(dim=-1).item()
    predicted_label = label_mapping.get(predicted_class, "Unknown")

    # Output results
    print(f"\nInput text: {text}")
    print(f"Predicted class: {predicted_class} ({predicted_label})")
    print(f"Probabilities: {probabilities}")

if __name__ == "__main__":
    main()
