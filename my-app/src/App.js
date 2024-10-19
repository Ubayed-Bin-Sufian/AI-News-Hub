import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [combinedSummary, setCombinedSummary] = useState("");
  const [error, setError] = useState("");

  // URLs for AI news
  const newsUrls = [
    'https://news.mit.edu/topic/artificial-intelligence2', // MIT AI News
    'https://techcrunch.com/category/artificial-intelligence/', // TechCrunch AI News
    'https://www.artificialintelligence-news.com/' // AI News
  ];

  // Function to fetch the combined news summary when the component loads
  useEffect(() => {
    const fetchCombinedNewsSummary = async () => {
      try {
        // Send a POST request to the backend with the list of news URLs
        const response = await axios.post('http://localhost:5000/AI_news', {
          urls: newsUrls // Send all URLs as an array
        });
        
        setCombinedSummary(response.data['News Summary: ']); // Assuming the backend returns a key 'News Summary: '
      } catch (err) {
        setError("An error occurred while fetching the combined summary.");
        console.error(err);
      }
    };

    fetchCombinedNewsSummary(); // Call the fetch function when the component mounts
  }, []); // Empty dependency array to run effect only once when component mounts

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>AI Combined News Summary</h1>
      
      {combinedSummary ? (
        <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ccc', width: '80%', margin: 'auto' }}>
          <h2>Latest AI News</h2>
          <p>{combinedSummary}</p>
        </div>
      ) : (
        <p>Loading combined summary...</p>
      )}

      {error && (
        <div style={{ marginTop: '30px', color: 'red' }}>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default App;
