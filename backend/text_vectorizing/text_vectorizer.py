import pandas as pd
from backend.text_vectorizing.vectorizer_utils import vectorize_text, check_class_imbalance, load_vectorizer
import logging

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

logger = logging.getLogger(__name__)

def process_and_vectorize(input_type="origin_reddit", input_path=None, is_training=False):
    """
    Process and vectorize text data.
    
    Parameters:
    - input_type: "origin_reddit", or "origin_labeled_dataset"
    - input_path: required if input_type is "origin_labeled_dataset"
    - is_training: bool, whether in training mode
    """
    if input_type not in {"origin_reddit", "origin_labeled_dataset"}:
        raise ValueError("input_type must be 'origin_reddit', or 'origin_labeled_dataset'.")

    try:
        if input_type == "origin_reddit":
            # Load the posts data
            df = pd.read_csv("backend/data/posts.csv")
            texts = df["post_body"].fillna(df["post_title"]).fillna("").str.strip()
            labels = df.get("category", None)
            output_path = "backend/data/vectorized_posts.csv"

            # Load the comments data
            df = pd.read_csv("backend/data/comments.csv")
            texts = df["comment_body"].fillna("").str.strip()
            labels = df.get("category", None)
            output_path = "backend/data/vectorized_comments.csv"

        elif input_type == "origin_labeled_dataset":
            if input_path is None:
                raise ValueError("Must provide input_path for external dataset.")
            df = pd.read_csv(input_path)
            
            if "clean_comment" in df.columns:
                texts = df["clean_comment"].fillna("").str.strip()
            else:
                raise ValueError("'clean_comment' column not found in external dataset.")
            
            if "category" in df.columns:
                labels = df["category"]
            else:
                labels = None  # No labels in external dataset if "category" is missing
            
            output_path = "backend/data/vectorized_labeled.csv"

    except FileNotFoundError as e:
        logger.error("Error loading data: %s", e)
        return

    # Filter out empty texts
    texts = texts[texts != ""]
    
    # Align the labels with the filtered texts (if labels are provided)
    if labels is not None:
        labels = labels.loc[texts.index]

    # Check for class imbalance if labels exist
    if labels is not None:
        check_class_imbalance(labels)

    # Load the existing vectorizer if not training
    vectorizer = load_vectorizer() if not is_training else None

    # Vectorize the texts
    if not texts.empty:
        vectors, features, vectorizer = vectorize_text(texts, vectorizer, is_training)
        vectors_df = pd.DataFrame(vectors.toarray(), columns=features)
        
        # Add the labels to the vectorized data if they exist
        if labels is not None:
            vectors_df["category"] = labels.values
            
        # Save the vectorized data to the appropriate CSV file
        vectors_df.to_csv(output_path, index=False)
        logger.info("Vectorized data saved to %s", output_path)
        
        # Reurn the filtered DataFrame
        return texts

if __name__ == "__main__":
    process_and_vectorize(input_type="origin_reddit", input_path=None, is_training=False)
