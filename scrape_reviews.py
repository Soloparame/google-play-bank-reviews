from google_play_scraper import reviews
import pandas as pd
import time

def fetch_reviews(app_id, bank_name, count=400, batch_size=100):
    all_reviews = []
    next_token = None
    attempts = 0

    print(f"\nFetching reviews for: {bank_name} ({app_id})")

    while len(all_reviews) < count and attempts < 10:
        try:
            result, next_token = reviews(
                app_id,
                lang='en',
                country='us',
                count=batch_size,
                continuation_token=next_token
            )
            all_reviews.extend(result)
            print(f"→ Collected {len(all_reviews)} reviews for {bank_name}")
            time.sleep(1)
            if not next_token:
                break
        except Exception as e:
            print(f"⚠️ Error while fetching reviews for {bank_name}: {e}")
            attempts += 1
            time.sleep(2)

    data = []
    for r in all_reviews[:count]:
        data.append({
            'review': r.get('content', ''),
            'rating': r.get('score', ''),
            'date': r.get('at', ''),
            'bank': bank_name,
            'source': 'Google Play Store'
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    apps = {
        "com.chase.sig.android": "Chase",
        "com.wf.wellsfargomobile": "Wells Fargo",
        "com.infonow.bofa": "Bank of America"  # ✅ corrected App ID
    }

    frames = []
    for app_id, bank_name in apps.items():
        df = fetch_reviews(app_id, bank_name, count=400)
        frames.append(df)
        print(f"✅ Finished {bank_name}: {len(df)} reviews")

    result_df = pd.concat(frames, ignore_index=True)
    result_df.to_csv("raw_reviews.csv", index=False)
    print("\n✅ All reviews saved to raw_reviews.csv")
