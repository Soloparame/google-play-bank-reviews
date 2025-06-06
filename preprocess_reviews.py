import pandas as pd

def preprocess(file_path="raw_reviews.csv", output_path="clean_reviews.csv"):
    df = pd.read_csv(file_path)

    # Drop duplicates
    df.drop_duplicates(subset=['review', 'rating', 'date', 'bank'], inplace=True)

    # Drop missing reviews or ratings
    df.dropna(subset=['review', 'rating'], inplace=True)

    # Normalize date format to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # Final cleanup
    df = df[['review', 'rating', 'date', 'bank', 'source']]

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned reviews to {output_path}")
    print(f"Total reviews after cleaning: {len(df)}")
    return df

if __name__ == "__main__":
    preprocess()
