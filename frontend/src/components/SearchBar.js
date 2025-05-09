import React, { useState } from "react";
import "./SearchBar.css";
import SentimentResults from "./SentimentResults";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    setSentimentData(null);

    try {
      // TODO: Replace with actual API call
      // Simulating API call with mock data
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockData = [65, 20, 15]; // [positive, neutral, negative]
      setSentimentData(mockData);
    } catch (error) {
      console.error('Error fetching sentiment data:', error);
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
