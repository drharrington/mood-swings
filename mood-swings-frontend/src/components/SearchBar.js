import React, { useState } from "react";
import "./SearchBar.css";

const SearchBar = () => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    alert(`Searching sentiment for: ${query}`);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Search a brand..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input"
      />
      <button onClick={handleSearch} className="search-btn">
        Analyze
      </button>
    </div>
  );
};

export default SearchBar;
