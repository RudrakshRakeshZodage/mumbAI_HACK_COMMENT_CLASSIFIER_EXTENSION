import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

def train_and_save(csv_path, vectorizer_path, model_path):
    df = pd.read_csv(csv_path)
    X = df['text'].astype(str)
    y = df['generated']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # Train the classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_tfidf, y_train)

    # Save fitted vectorizer and model
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(clf, model_path)

    print(f"✅ Saved fitted vectorizer to {vectorizer_path}")
    print(f"✅ Saved trained model to {model_path}")

if __name__ == "__main__":
    train_and_save("../data/AI_Human.csv", "../models/vectorizer.pkl", "../models/clf.pkl")
