import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const SentimentChart = ({ data }) => {
  const chartData = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        data: data,
        backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
      },
    ],
  };

  return (
    <div>
      <h2>Sentiment Analysis</h2>
      <Pie data={chartData} />
    </div>
  );
};

export default SentimentChart;
