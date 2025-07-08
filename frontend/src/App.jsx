import './App.css'
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
      fetch('https://api-last-minute-tennis.com/scrape/location=6')
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => console.error('API error:', err));
    }, []);

    return (
      <div>
        <h1>Data from FastAPI backend:</h1>
        <pre>{data ? JSON.stringify(data, null, 2) : 'Loading...'}</pre>
      </div>
    );
  }

export default App;
