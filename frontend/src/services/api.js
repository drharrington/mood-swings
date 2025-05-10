export const fetchSentimentData = async (brandName) => {
  try {
    const response = await fetch("https://mood-swings-api.onrender.com/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ brand_name: brandName }),
    });
    return await response.json();
  } catch (error) {
    console.error("Error fetching sentiment data:", error);
    return null;
  }
};
