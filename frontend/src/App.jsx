import './App.css'
import { useEffect, useState } from 'react';

function App() {
  const [count, setCount] = useState(0)

  useEffect(() => {
      fetch('http://3.104.109.133/scrape/location=6')
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
