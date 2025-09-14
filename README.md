# 🧠 AI Comment Classifier – Chrome Extension

A Google Chrome extension + Flask backend that **classifies comments as “AI-generated” or “Human-written”** in real time using Natural Language Processing (NLP) and Machine Learning.

---

## 🚀 Features
- 🔍 **Real-time classification** of any text/comment
- 🧩 **Google Chrome Extension** front-end for easy use
- ⚡ **Flask REST API** backend serving the ML model
- 📊 Shows **prediction confidence (%)**
- 🌐 Cross-origin ready using **Flask-CORS**

---

## 🛠️ Tech Stack
| Layer        | Technology |
|--------------|-----------|
| Frontend     | Chrome Extension, HTML, CSS, JavaScript |
| Backend      | Python Flask API |
| Machine Learning | TF-IDF Vectorizer + Logistic Regression |
| Data Science | scikit-learn, joblib |

---

## 🧬 Machine Learning Pipeline

1. **Pre-processing**
   - Clean and normalize text (lower-casing, punctuation removal, etc.)
   - Transform text into numerical features using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

2. **Model**
   - **Logistic Regression** classifier.
   - **Binary Cross-Entropy (Log Loss)** used as the loss function.
   - **Regularization** (L2) applied to avoid overfitting.

3. **Output**
   - Probability score between 0 and 1.
   - Threshold = 0.5 →  
     - **AI** if probability ≥ 0.5  
     - **Human** otherwise.

4. **Persistence**
   - Trained model (`clf.pkl`) and vectorizer (`vectorizer.pkl`) stored with **joblib** and loaded by the Flask API.

---

