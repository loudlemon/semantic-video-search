// APP.js
import React, { useState } from 'react';
import './App.css';

// --- Utility for simulating API calls ---
const simulateApiCall = (endpoint, data) => {
  console.log(`[API SIM] Request to /${endpoint} with data:`, data);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: `Operation successful on ${endpoint}` });
    }, 1500); // Simulate network latency
  });
};


function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [status, setStatus] = useState('System initialized. Ready to load assets.');
  const [isSearching, setIsSearching] = useState(false);

  const updateStatus = (message) => {
    setStatus(message);
    console.log(`STATUS UPDATE: ${message}`);
  };

  // --- Handlers ---

  const handleFileUpload = async (type) => {
    const fileName = type === 'video' ? 'TestVideo.mp4' : 'EtalonImage.jpg';
    updateStatus(`Uploading ${type} file: ${fileName}...`);
    
    try {
      const result = await simulateApiCall('upload', { file_name: fileName, type });
      if (result.success) {
        updateStatus(`${fileName} uploaded successfully. Ready to search.`);
      }
    } catch (error) {
      updateStatus(`Error uploading ${type}: Check console.`);
      console.error(error);
    }
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      updateStatus("Error: Search term cannot be empty.");
      return;
    }
    
    setIsSearching(true);
    updateStatus(`Executing semantic search for: "${searchTerm}"...`);

    try {
      const result = await simulateApiCall('search', { query: searchTerm });
      if (result.success) {
        updateStatus('Search complete. Found 12 relevant semantic matches.');
      }
    } catch (error) {
      updateStatus("Search failed. Backend error.");
      console.error(error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="app-container">
      <video
        className="bg-video"
        src="/test_video.mp4"
        autoPlay
        muted
        loop
        playsInline
      />
      <div className="content-area">
        
        {/* 1. Title */}
        <h1 className="app-title">Semantic Video Search Service</h1>

        {/* 2. Upload Controls (Above Search Bar) */}
        <div className="upload-controls">
          <button 
            className="menu-button upload-button" 
            onClick={() => handleFileUpload('video')}
            disabled={isSearching}
          >
            Upload Video
          </button>
          <button 
            className="menu-button upload-button" 
            onClick={() => handleFileUpload('etalon_image')}
            disabled={isSearching}
          >
            Upload Etalon Image
          </button>
        </div>

        {/* 3. Search Bar & Button */}
        <div className="search-area">
          <input
            type="text"
            className="search-input"
            placeholder="Enter semantic query here..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === 'Enter' && !isSearching) {
                    handleSearch();
                }
            }}
            disabled={isSearching}
          />
          <button 
            className="menu-button"
            onClick={handleSearch}
            disabled={isSearching}
          >
            {isSearching ? 'Processing...' : 'Search'}
          </button>
        </div>

        {/* 4. Status Bar */}
        <div className="status-bar">
          Status: {status}
        </div>

      </div>
    </div>
  );
}

export default App;
