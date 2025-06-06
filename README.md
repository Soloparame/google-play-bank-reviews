# Google Play Bank Reviews

## Task 1: Data Collection and Preprocessing

### Objective
Scrape and clean 1200+ reviews from Google Play Store for three banking apps.

### Tools Used
- google-play-scraper
- pandas
- Python

### Steps
1. Scraped 400+ reviews each for Chase, Wells Fargo, and Bank of America.
2. Removed duplicates and missing values.
3. Normalized dates to YYYY-MM-DD.
4. Exported to CSV.

### Files
- `scrape_reviews.py`: Collects reviews using `google-play-scraper`
- `preprocess_reviews.py`: Cleans and saves the dataset
- `raw_reviews.csv`: Raw scraped data
- `clean_reviews.csv`: Cleaned and structured dataset
