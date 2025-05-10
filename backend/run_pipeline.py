import logging
from backend.scraper.reddit_scraper import run_scraper
from backend.text_vectorizing.text_vectorizer import process_and_vectorize
from backend.models.sentiment_model import predict_sentiment
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def run_pipeline(brand_name):
    """Run the sentiment analysis pipeline and return results."""
    try:
        # Step 1: Scrape data
        logger.info(f"Scraping data for brand: {brand_name}")
        run_scraper(brand_name)

        # Step 2: Vectorize data
        logger.info("Vectorizing Reddit data...")
        texts = process_and_vectorize(input_type="origin_reddit", is_training=False)

        # Step 3: Predict sentiment
        logger.info("Predicting sentiment...")
        predictions = predict_sentiment(texts)

        # Step 4: Add predictions to DataFrame
        texts = texts.reset_index(drop=True)
        df = pd.DataFrame({"text": texts, "sentiment": predictions})
        df["sentiment_label"] = df["sentiment"].map(
            {1: "Positive", 0: "Neutral", -1: "Negative"}
        )

        # Step 5: Calculate sentiment counts
        sentiment_counts = df["sentiment"].value_counts()
        positive_count = sentiment_counts.get(1, 0)
        neutral_count = sentiment_counts.get(0, 0)
        negative_count = sentiment_counts.get(-1, 0)

        # Step 6: Calculate overall sentiment
        overall_sentiment = df["sentiment"].value_counts().idxmax()
        overall_label = {1: "Positive", 0: "Neutral", -1: "Negative"}[overall_sentiment]

        # Step 7: Return results
        results = {
            "overall_sentiment": overall_label,
            "positive_count": int(positive_count),
            "neutral_count": int(neutral_count),
            "negative_count": int(negative_count),
        }
        return results

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    brand_name = input("Enter the brand name for sentiment analysis: ")
    results = run_pipeline(brand_name)
    print("Sentiment Analysis Results:")
    print(results)
