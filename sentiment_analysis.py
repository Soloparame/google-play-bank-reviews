from transformers import pipeline
import pandas as pd

def compute_sentiment(df, text_col="review"):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    sentiments = classifier(df[text_col].tolist(), truncation=True)

    df["sentiment_label"] = [s["label"] for s in sentiments]
    df["sentiment_score"] = [s["score"] for s in sentiments]
    return df

if __name__ == "__main__":
    df = pd.read_csv("raw_reviews.csv")
    df = compute_sentiment(df)
    df.to_csv("sentiment_reviews.csv", index=False)
    print("✅ Sentiment scores saved to sentiment_reviews.csv")
