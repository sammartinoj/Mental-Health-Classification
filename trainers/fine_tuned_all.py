import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, set_seed
from sklearn.metrics import f1_score
from datasets import Dataset

def train_model():
    set_seed(42)

    # Define file paths
    train_file = "train_MH.csv"
    val_file = "val_MH.csv"
    test_file = "test_MH.csv"

    # Define model and training parameters
    model_name = "bert-base-uncased"
    output_dir = "./fine_tuned_all"
    num_epochs = 5
    batch_size = 16
    learning_rate = 1e-5

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
        greater_is_better=True,
        #gradient_accumulation_steps=2
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
    train_model()

