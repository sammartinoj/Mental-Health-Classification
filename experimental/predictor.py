import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def load_model_and_tokenizer(model_dir):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    return tokenizer, model

def predict(text, model, tokenizer, label_mapping):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction_idx = logits.argmax(dim=-1).item()
        prediction_label = label_mapping.get(prediction_idx, "Unknown")
    return prediction_idx, prediction_label

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform inference with a trained model.")
    parser.add_argument("--model", type=str, choices=["downsampled", "disorder_only"], required=True,
                        help="Choose the model to use: 'downsampled' or 'disorder_only'.")
    parser.add_argument("--text", type=str, required=True, help="Input text for inference.")
    
    args = parser.parse_args()

    # Map model names to directories
    model_dirs = {
        "downsampled": "downsampled_model",
        "disorder_only": "disorder_only_downsampled_model"
    }
    model_dir = model_dirs[args.model]

    # Define the label mapping
    label_mapping = {
        0: 'Anxiety',
        1: 'Bipolar',
        2: 'Depression',
        3: 'Normal',
        4: 'Personality-disorder',
        5: 'Stress',
        6: 'Suicidal'
    }
    tokenizer, model = load_model_and_tokenizer(model_dir)
    model.to("cuda" if torch.cuda.is_available() else "cpu")

    prediction_idx, prediction_label = predict(args.text, model, tokenizer, label_mapping)
    print(f"Prediction Index: {prediction_idx}")
    print(f"Prediction Label: {prediction_label}")

