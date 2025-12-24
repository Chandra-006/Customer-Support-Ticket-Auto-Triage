import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import json

# Load dataset
data = pd.read_csv("data/tickets.csv")

# Combine Subject and Description
data["text"] = data["Subject"] + " " + data["Description"]

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

data["clean_text"] = data["text"].apply(clean_text)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words="english"
)

X = vectorizer.fit_transform(data["clean_text"])
y = data["Category"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}\n")

# Train model
print("Training model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1_score, support = precision_recall_fscore_support(
    y_test, y_pred, average=None, zero_division=0
)

# Get unique categories
categories = sorted(y.unique())
metrics_per_category = {}

for i, category in enumerate(categories):
    metrics_per_category[category] = {
        "precision": float(precision[i]),
        "recall": float(recall[i]),
        "f1_score": float(f1_score[i]),
        "support": int(support[i])
    }

# Calculate macro averages
macro_precision = precision.mean()
macro_recall = recall.mean()
macro_f1 = f1_score.mean()

# Overall metrics
overall_metrics = {
    "accuracy": float(accuracy),
    "macro_avg_precision": float(macro_precision),
    "macro_avg_recall": float(macro_recall),
    "macro_avg_f1_score": float(macro_f1)
}

# Print evaluation results
print("=" * 60)
print("MODEL EVALUATION RESULTS")
print("=" * 60)
print(f"\nOverall Accuracy: {accuracy:.4f}")
print(f"\nMacro-Averaged Metrics:")
print(f"  Precision: {macro_precision:.4f}")
print(f"  Recall: {macro_recall:.4f}")
print(f"  F1-Score: {macro_f1:.4f}")

print(f"\nPer-Category Metrics:")
print("-" * 60)
for category in categories:
    idx = list(categories).index(category)
    print(f"\n{category}:")
    print(f"  Precision: {precision[idx]:.4f}")
    print(f"  Recall: {recall[idx]:.4f}")
    print(f"  F1-Score: {f1_score[idx]:.4f}")
    print(f"  Support: {support[idx]}")

print("\n" + "=" * 60)
print("Detailed Classification Report:")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=categories))

# Save model & vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save evaluation metrics to JSON file
evaluation_results = {
    "overall_metrics": overall_metrics,
    "per_category_metrics": metrics_per_category
}

with open("evaluation_metrics.json", "w") as f:
    json.dump(evaluation_results, f, indent=2)

print("\n✅ Model and vectorizer saved successfully!")
print("✅ Evaluation metrics saved to evaluation_metrics.json")
