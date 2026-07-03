import os
import re
import string
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.strip()
    return text


def main():
    dataset_path = "data/spam.csv"

    if not os.path.exists(dataset_path):
        print("Dataset not found. Please place spam.csv inside the data folder.")
        return

    # Some spam.csv files have encoding issues, so latin-1 is safer
    df = pd.read_csv(dataset_path, encoding="latin-1")

    # Keep only useful columns
    df = df[["v1", "v2"]]
    df.columns = ["label", "message"]

    # Convert labels: ham = 0, spam = 1
    df["label"] = df["label"].map({"ham": 0, "spam": 1})

    # Clean messages
    df["clean_message"] = df["message"].apply(clean_text)

    X = df["clean_message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    vectorizer = TfidfVectorizer(stop_words="english", max_features=3000)

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Model 1: Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_tfidf, y_train)
    nb_pred = nb_model.predict(X_test_tfidf)

    print("\nNaive Bayes Accuracy:", accuracy_score(y_test, nb_pred))
    print("\nNaive Bayes Classification Report:")
    print(classification_report(y_test, nb_pred))

    # Model 2: Logistic Regression
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train_tfidf, y_train)
    lr_pred = lr_model.predict(X_test_tfidf)

    print("\nLogistic Regression Accuracy:", accuracy_score(y_test, lr_pred))
    print("\nLogistic Regression Classification Report:")
    print(classification_report(y_test, lr_pred))

    print("\nConfusion Matrix for Logistic Regression:")
    print(confusion_matrix(y_test, lr_pred))

    # Save the better model
    os.makedirs("models", exist_ok=True)

    joblib.dump(nb_model, "models/spam_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")

    print("\nModel and vectorizer saved successfully inside models folder.")


if __name__ == "__main__":
    main()