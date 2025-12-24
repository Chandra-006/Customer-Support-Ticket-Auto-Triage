# Customer Support Ticket Auto-Triage

An advanced machine learning project focused on revolutionizing customer support through intelligent ticket classification and automated routing systems.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technical Requirements](#technical-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Evaluation](#model-evaluation)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Performance Metrics](#performance-metrics)

## 🎯 Project Overview

This project automates the initial processing of customer support tickets by classifying them into predefined categories, reducing manual effort and accelerating resolution times.

### Key Ticket Categories

The model classifies tickets into 5 categories:

- **Bug Report**: Software defects or errors requiring immediate action
- **Feature Request**: User suggestions for new functionalities and enhancements
- **Technical Issue**: Problems requiring specialized technical assistance
- **Billing Inquiry**: Questions related to invoices, payments, and subscriptions
- **Account Management**: Issues regarding user accounts, profiles, and access controls

## ✨ Features

- ✅ Automated ticket classification using machine learning
- ✅ RESTful API for real-time predictions
- ✅ Comprehensive model evaluation metrics
- ✅ Latency measurement for performance monitoring
- ✅ Confidence scores for predictions
- ✅ Production-ready error handling

## 🔧 Technical Requirements

- **Python**: 3.8 or higher
- **Key Libraries**:
  - scikit-learn (1.8.0)
  - pandas (2.3.3)
  - numpy (2.4.0)
  - Flask (3.1.2)
  - NLTK (3.9.2) - Optional, for advanced text processing

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd customer-support-ticket-auto-triage
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Model

Before using the API, you need to train the model:

```bash
python train.py
```

This will:
- Load the training data from `data/tickets.csv`
- Train a Logistic Regression model with TF-IDF vectorization
- Evaluate the model and generate metrics
- Save the model (`model.pkl`) and vectorizer (`vectorizer.pkl`)
- Generate `evaluation_metrics.json` with performance metrics

## 🚀 Usage

### Starting the API Server

```bash
python app.py
```

The API will start on `http://localhost:5000`

### Making Predictions

#### Using cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The app crashes when I try to open it"}'
```

#### Using Python

```python
import requests

url = "http://localhost:5000/predict"
data = {"text": "The app crashes when I try to open it"}

response = requests.post(url, json=data)
print(response.json())
```

#### Example Response

```json
{
  "ticket_text": "The app crashes when I try to open it",
  "predicted_category": "Bug Report",
  "confidence": 0.9234,
  "latency_ms": 12.45,
  "timestamp": "2025-01-XXTXX:XX:XX.XXXXXX"
}
```

## 📚 API Documentation

### Endpoints

#### `GET /`

Health check endpoint.

**Response:**
```json
{
  "status": "running",
  "message": "Customer Support Ticket Auto-Triage API is running!",
  "timestamp": "2025-01-XXTXX:XX:XX.XXXXXX"
}
```

#### `POST /predict`

Classify a support ticket.

**Request Body:**
```json
{
  "text": "Your ticket text here"
}
```

**Response:**
```json
{
  "ticket_text": "Your ticket text here",
  "predicted_category": "Category Name",
  "confidence": 0.9234,
  "latency_ms": 12.45,
  "timestamp": "2025-01-XXTXX:XX:XX.XXXXXX"
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid input
- `500 Internal Server Error`: Server-side error

#### `GET /metrics`

Get model evaluation metrics.

**Response:**
```json
{
  "model_metrics": {
    "overall_metrics": {
      "accuracy": 0.95,
      "macro_avg_precision": 0.94,
      "macro_avg_recall": 0.93,
      "macro_avg_f1_score": 0.935
    },
    "per_category_metrics": {
      "Bug Report": {
        "precision": 0.92,
        "recall": 0.90,
        "f1_score": 0.91,
        "support": 6
      }
    }
  },
  "api_status": "operational"
}
```

## 📊 Model Evaluation

The model is evaluated using the following metrics:

### Evaluation Metrics

1. **Accuracy**: Overall correct predictions across all categories
2. **Precision**: Proportion of positive identifications that were correct
3. **Recall**: Proportion of actual positives that were identified correctly
4. **F1-Score**: Harmonic mean of precision and recall
5. **Latency**: API response time in milliseconds

### Viewing Evaluation Results

After training, evaluation metrics are:
- Printed to the console
- Saved to `evaluation_metrics.json`
- Available via the `/metrics` API endpoint

## 📁 Project Structure

```
customer-support-ticket-auto-triage/
│
├── app.py                      # Flask API application
├── train.py                    # Model training script
├── model.pkl                   # Trained model (generated)
├── vectorizer.pkl              # TF-IDF vectorizer (generated)
├── evaluation_metrics.json     # Model evaluation metrics (generated)
│
├── data/
│   └── tickets.csv            # Training dataset
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
└── venv/                      # Virtual environment (not in repo)
```

## 🔬 Methodology

### Data Preprocessing

1. **Text Combination**: Subject and Description fields are combined
2. **Text Cleaning**:
   - Convert to lowercase
   - Remove special characters (keep only letters and spaces)
   - Normalize whitespace

### Feature Engineering

- **TF-IDF Vectorization**: 
  - Maximum 1000 features
  - English stop words removed
  - Converts text to numerical features

### Model Architecture

- **Algorithm**: Logistic Regression
  - Maximum iterations: 1000
  - Random state: 42 (for reproducibility)
- **Train/Test Split**: 80/20 with stratification

### Training Process

1. Load and preprocess data
2. Split into training (80%) and testing (20%) sets
3. Fit TF-IDF vectorizer on training data
4. Train Logistic Regression model
5. Evaluate on test set
6. Save model and metrics

## 📈 Performance Metrics

Model performance is evaluated using:

- **Overall Accuracy**: Measures general model effectiveness
- **Per-Category Metrics**: Precision, Recall, and F1-Score for each category
- **Macro-Averaged Metrics**: Balanced evaluation across all categories
- **Latency**: Real-time prediction response time

## 🐛 Troubleshooting

### Model files not found

If you see errors about missing `model.pkl` or `vectorizer.pkl`:
```bash
python train.py
```

### Port already in use

If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)  # Change port
```

### Import errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📝 License

This project is part of a machine learning assessment.

## 👤 Author

Customer Support Ticket Auto-Triage Project

## 📧 Submission

**Submission Email:** support@levelmasters.ai  
**Subject Line:** "RdML Assessment – Support Ticket Auto-Triage – [Your Full Name]"

**Submission Requirements:**
- ✅ Code Repository: Git repository with clear commit messages
- ✅ Comprehensive README: Detailed setup, execution, and model usage
- ✅ Model & Data Access: Model checkpoint and data files easily accessible

**Repository:** https://github.com/Chandra-006/Customer-Support-Ticket-Auto-Triage.git

---

**Last Updated**: 2025-01-XX

