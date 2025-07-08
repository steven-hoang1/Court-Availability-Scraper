import './App.css'
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
      fetch('https://api-last-minute-tennis.com/scrape/location=55')
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => console.error('API error:', err));
    }, []);

    return (
    <div>
      <h1>Centennial Park</h1>
      {data ? (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Courts Available</th>
            </tr>
          </thead>
          <tbody>
            {data.map((slot, idx) => (
              <tr key={idx}>
                <td>{slot.date}</td>
                <td>{slot.time}</td>
                <td>{slot.courts_available}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
  }

export default App;
