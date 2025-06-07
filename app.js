import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setPrediction('');
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/classify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Failed to classify resume. Is your backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '40px' }}>
      <h1>Resume Classifier</h1>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload}>Classify Resume</button>
      <br /><br />
      {loading ? <p>Classifying...</p> : prediction && <h2>Prediction: {prediction}</h2>}
    </div>
  );
}

export default App;
