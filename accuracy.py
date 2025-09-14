import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@\w+|\#','', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text.lower().strip()

def train_advanced(csv_path, vectorizer_path, model_path):
    # Load and clean data
    df = pd.read_csv(csv_path)
    df.dropna(subset=['text', 'generated'], inplace=True)
    df['text'] = df['text'].astype(str).apply(clean_text)

    # Features and labels
    X = df['text']
    y = df['generated']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Logistic Regression with GridSearchCV
    params = {'C': [0.1, 1, 10], 'max_iter': [500, 1000]}
    grid = GridSearchCV(LogisticRegression(class_weight='balanced'), param_grid=params, cv=5)
    grid.fit(X_train_tfidf, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)

    print("\n✅ Accuracy:", f"{acc * 100:.2f}%")
    print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
    print("\n📉 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save model and vectorizer
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(best_model, model_path)
    print(f"\n💾 Saved vectorizer to {vectorizer_path} and model to {model_path}")

if __name__ == "__main__":
    train_advanced("../data/AI_Human.csv", "../models/vectorizer.pkl", "../models/clf.pkl")
