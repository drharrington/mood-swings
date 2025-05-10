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

  let sentimentLabel = '';
  let sentimentColor = '';
  if (data && data.length === 3) {
    const max = Math.max(...data);
    const idx = data.indexOf(max);
    if (idx === 0) {
      sentimentLabel = 'Positive';
      sentimentColor = '#4CAF50'; // green
    } else if (idx === 1) {
      sentimentLabel = 'Neutral';
      sentimentColor = '#FFC107'; // yellow
    } else if (idx === 2) {
      sentimentLabel = 'Negative';
      sentimentColor = '#F44336'; // red
    }
  }

  return (
    <div>
      {sentimentLabel && (
        <div style={{ fontWeight: 'bold' }}>
          Sentiment: <span style={{ color: sentimentColor }}>{sentimentLabel}</span>
        </div>
      )}
      <h2>Sentiment Analysis</h2>
      <Pie data={chartData} />
    </div>
  );
};

export default SentimentChart;
