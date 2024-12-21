import argparse
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, set_seed
from sklearn.metrics import f1_score

# Our training function
def train_model(train_file, val_file, test_file, model_name, output_dir, num_epochs, batch_size, learning_rate):
    set_seed(42)

    # Load data
    df_train = pd.read_csv(train_file).dropna(subset=['status']).drop(columns=["Unnamed: 0"])
    df_val = pd.read_csv(val_file).dropna(subset=['status']).drop(columns=["Unnamed: 0"])
    df_test = pd.read_csv(test_file).dropna(subset=['status']).drop(columns=["Unnamed: 0"])

    df_train['labels'] = pd.factorize(df_train['status'])[0]
    df_val['labels'] = pd.factorize(df_val['status'])[0]
    df_test['labels'] = pd.factorize(df_test['status'])[0]

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_function(examples):
        return tokenizer(examples["statement"], padding="max_length", truncation=True)

    # Tokenize datasets
    from datasets import Dataset
    train_dataset = Dataset.from_pandas(df_train).map(tokenize_function, batched=True)
    val_dataset = Dataset.from_pandas(df_val).map(tokenize_function, batched=True)
    test_dataset = Dataset.from_pandas(df_test).map(tokenize_function, batched=True)

    # Model setup
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(df_train['labels'].unique()))

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        logging_dir="./logs",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True
    )

    # Metrics
    def compute_metrics(pred):
        logits, labels = pred
        predictions = logits.argmax(axis=-1)
        f1 = f1_score(labels, predictions, average="weighted")
        return {"f1": f1}

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # Train and save
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print("Training completed. Model and tokenizer saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a mental health classification model.")
    parser.add_argument("--train_file", type=str, required=True, help="Path to the training data CSV.")
    parser.add_argument("--val_file", type=str, required=True, help="Path to the validation data CSV.")
    parser.add_argument("--test_file", type=str, required=True, help="Path to the test data CSV.")
    parser.add_argument("--model_name", type=str, default="bert-base-uncased", help="Hugging Face model name.")
    parser.add_argument("--output_dir", type=str, default="./fine_tuned_model", help="Directory to save the model.")
    parser.add_argument("--num_epochs", type=int, default=5, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size.")
    parser.add_argument("--learning_rate", type=float, default=1e-5, help="Learning rate.")

    args = parser.parse_args()
    train_model(args.train_file, args.val_file, args.test_file, args.model_name, args.output_dir, args.num_epochs, args.batch_size, args.learning_rate)

