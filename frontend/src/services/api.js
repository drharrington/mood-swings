export const fetchSentimentData = async (brandName) => {
  try {
    const response = await fetch("http://localhost:5000/analyze", {
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
