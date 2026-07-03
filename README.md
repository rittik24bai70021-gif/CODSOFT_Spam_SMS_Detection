# Spam SMS Detection

**Overview:**
- **Project:**: A lightweight SMS spam detector that uses TF-IDF features and classic machine learning to classify SMS messages as spam or ham (legitimate). The project includes a Streamlit UI for live testing and utilities to train and save models.

**What Is Used:**
- **Language**: Python 3.8+
- **Core libraries**: pandas, numpy, scikit-learn, joblib
- **Web UI**: Streamlit (used by `app.py`)
- **Modeling**: `TfidfVectorizer`, `MultinomialNB`, `LogisticRegression` (in `train_model.py`)
- **Utilities**: `re`, `string`, `datetime` (for preprocessing and reporting)

**Dataset:**
- The project expects the SMS Spam Collection dataset CSV at [data/spam.csv](data/spam.csv). The training script loads this file (latin-1 safe read) and uses columns `v1` and `v2` which are renamed to `label` and `message`.

**Folder Structure (important files):**
- [app.py](app.py): Streamlit app for demo and live prediction.
- [train_model.py](train_model.py): Training pipeline (cleaning, TF-IDF, training, evaluation, saving model).
- [requirements.txt](requirements.txt): Minimal Python dependencies.
- [data/spam.csv](data/spam.csv): Dataset (not included by default).
- models/: Saved `spam_model.pkl` and `vectorizer.pkl` after training.
- screenshots/: Example UI screenshots.

**Installation:**
1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate      # Windows (PowerShell)
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure the dataset is present at `data/spam.csv`.

**Train the Model:**
- The training script will clean text, vectorize with TF-IDF (max_features=3000), train Naive Bayes and Logistic Regression, print metrics, and save the model and vectorizer to `models/`.

```bash
python train_model.py
```

After running, check the `models/` directory for `spam_model.pkl` and `vectorizer.pkl`.

**Run the App (Demo):**
- Start the Streamlit app to use the interactive UI:

```bash
streamlit run app.py
```

- In the UI you can:
	- Enter or paste an SMS message to analyze.
	- Use quick examples (Spam, Ham, Offer).
	- See spam/ham confidence, detected suspicious words, risk level, and safety suggestions.
	- Download a prediction report.

**Implementation Notes:**
- Text cleaning: `clean_text()` lowercases, removes URLs, numbers, and punctuation.
- Spam keywords: `count_spam_keywords()` checks for common spam terms; `contains_link()` detects link-like patterns.
- Risk & suggestions: The app computes a simple risk level from predicted spam confidence and provides human-readable safety suggestions.
- Model loading: `app.py` expects `models/spam_model.pkl` and `models/vectorizer.pkl` to exist.

**Reproducibility & Tips:**
- If using a custom dataset, ensure it follows the same two-column convention (label, message) or adapt `train_model.py` accordingly.
- To retrain with different hyperparameters, modify `train_model.py` (e.g., change `TfidfVectorizer` settings or classifier parameters).

**Security & Privacy:**
- Do not upload or expose real private messages publicly. This project is intended for educational/demo purposes.

**Screenshots:**
- See the `screenshots/` folder for UI examples.

**License & Credits:**
- Use or redistribute under your chosen license. Acknowledge the original SMS Spam Collection dataset when publishing results.

**Need changes?**
- If you'd like a shorter or more detailed section (e.g., expanded model metrics, hyperparameter examples, CI instructions), tell me which parts to extend.

