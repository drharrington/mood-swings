export const fetchSentimentData = async () => {
  try {
    const response = await fetch("http://localhost:5000/sentiment"); // Backend URL
    return await response.json();
  } catch (error) {
    console.error("Error fetching sentiment data:", error);
    return [50, 30, 20]; // Default fallback values
  }
};
