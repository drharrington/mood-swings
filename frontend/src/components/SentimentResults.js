import React from 'react';
import { motion } from 'framer-motion';
import SentimentChart from './SentimentChart';
import './SentimentResults.css';

const SentimentResults = ({ data, isLoading }) => {
  if (isLoading) {
    return (
      <motion.div
        className="sentiment-results loading"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="loading-spinner"></div>
        <p>Analyzing sentiment...</p>
      </motion.div>
    );
  }

  if (!data) return null;

  const [positive, neutral, negative] = data;
  const total = positive + neutral + negative;

  const percentages = {
    positive: ((positive / total) * 100).toFixed(1),
    neutral: ((neutral / total) * 100).toFixed(1),
    negative: ((negative / total) * 100).toFixed(1)
  };

  return (
    <motion.div
      className="sentiment-results"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      <div className="chart-container">
        <SentimentChart data={data} />
      </div>

      <div className="sentiment-details">
        <motion.div
          className="sentiment-stat"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <h3>Positive</h3>
          <p className="percentage positive">{percentages.positive}%</p>
          <p className="count">{positive} mentions</p>
        </motion.div>

        <motion.div
          className="sentiment-stat"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <h3>Neutral</h3>
          <p className="percentage neutral">{percentages.neutral}%</p>
          <p className="count">{neutral} mentions</p>
        </motion.div>

        <motion.div
          className="sentiment-stat"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <h3>Negative</h3>
          <p className="percentage negative">{percentages.negative}%</p>
          <p className="count">{negative} mentions</p>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default SentimentResults;
