import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import string

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop and token.lemma_ not in string.punctuation
    ]
    return " ".join(tokens)

def extract_keywords_tfidf(df, text_col="review", top_n=10):
    tfidf = TfidfVectorizer(max_df=0.8, min_df=5, ngram_range=(1, 2))
    X = tfidf.fit_transform(df[text_col])
    feature_array = tfidf.get_feature_names_out()

    scores = X.sum(axis=0).A1
    ranked = sorted(zip(feature_array, scores), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in ranked[:top_n]]

if __name__ == "__main__":
    df = pd.read_csv("sentiment_reviews.csv")
    df["cleaned_review"] = df["review"].fillna("").apply(preprocess_text)

    themes = {}
    for bank in df["bank"].unique():
        bank_df = df[df["bank"] == bank]
        keywords = extract_keywords_tfidf(bank_df, text_col="cleaned_review")
        themes[bank] = keywords
        print(f"\n🔍 {bank} keywords:", keywords)
# Grouping dictionary
themes_grouping = {
    "login": "Account Access",
    "password": "Account Access",
    "sign in": "Account Access",
    "transfer": "Transaction Performance",
    "payment": "Transaction Performance",
    "slow": "Performance",
    "lag": "Performance",
    "crash": "Reliability",
    "freeze": "Reliability",
    "customer service": "Customer Support",
    "support": "Customer Support",
    "agent": "Customer Support",
    "ui": "User Experience",
    "design": "User Experience",
    "interface": "User Experience"
}

# Function to assign themes
def assign_theme(review, themes_grouping):
    matched_themes = set()
    review_lower = review.lower()
    for keyword, theme in themes_grouping.items():
        if keyword in review_lower:
            matched_themes.add(theme)
    return ", ".join(matched_themes) if matched_themes else "Other"

# Assign themes to each review
df["identified_theme"] = df["review"].fillna("").apply(lambda x: assign_theme(x, themes_grouping))

df.to_csv("thematic_reviews.csv", index=False)
