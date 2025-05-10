import React, { useState } from "react";
import "./SearchBar.css";
import SentimentResults from "./SentimentResults";
import { fetchSentimentData } from "../services/api";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    setSentimentData(null);

    try {
      const result = await fetchSentimentData(query);
      // result should have overall_sentiment, positive_count, neutral_count, negative_count
      if (result && typeof result === 'object') {
        setSentimentData([
          result.positive_count || 0,
          result.neutral_count || 0,
          result.negative_count || 0
        ]);
      } else {
        setSentimentData([0, 0, 0]);
      }
    } catch (error) {
      console.error('Error fetching sentiment data:', error);
      setSentimentData([0, 0, 0]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="search-section">
      <div className="search-container">
        <input
          type="text"
          placeholder="Search a brand..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button
          onClick={handleSearch}
          className="search-btn"
          disabled={isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      <SentimentResults
        data={sentimentData}
        isLoading={isLoading}
      />
    </div>
  );
};

export default SearchBar;
