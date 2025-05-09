import React, { useState } from "react";
import { motion } from "framer-motion";
import { TypeAnimation } from "react-type-animation";
import SearchBar from "./SearchBar";
import "./LandingPage.css";
const LandingPage = () => {
  const [showSearch, setShowSearch] = useState(false);

  return (
    <div className="landing-container">
      {/* Logo and Typing animation for "Mood Swing" */}
      <div className="title-row">
        <img
          src={process.env.PUBLIC_URL + '/mood_logo.png'}
          alt="Mood Swings Logo"
          className="mood-logo"
        />
        <TypeAnimation
          sequence={[
            "Mood Swing", // Text to type out
            2000, // Pause for 2 seconds
          ]}
          wrapper="h1"
          cursor={true}
          repeat={0} // Type once only
          className="title"
        />
      </div>

      {/* Description below title */}
      <motion.p
        className="description"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2, duration: 2 }}
      >
        Learn about the sentiment towards your brand of choice based on Reddit
        discussions.
      </motion.p>

      {/* Fade-in "Get Sentiment" button */}
      {!showSearch && (
        <motion.button
          className="sentiment-btn"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 3, duration: 2 }}
          onClick={() => setShowSearch(true)}
        >
          Get Sentiment
        </motion.button>
      )}

      {/* Slide-down search bar */}
      {showSearch && (
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1 }}
        >
          <SearchBar />
        </motion.div>
      )}
    </div>
  );
};

export default LandingPage;
