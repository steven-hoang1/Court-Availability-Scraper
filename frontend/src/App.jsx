import './App.css'
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
      fetch('https://api-last-minute-tennis.com/scrape/location=2')
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => console.error('API error:', err));
    }, []);

    return (
      <div className={styles.container}>
        <h1 className={styles.heading}>Surry Hills</h1>
        {data ? (
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th className={styles.th}>Date</th>
                  <th className={styles.th}>Time</th>
                  <th className={styles.th}>Courts Available</th>
                </tr>
              </thead>
              <tbody>
                {data.map((slot, idx) => (
                  <tr key={idx} className={styles.tr}>
                    <td className={styles.td}>{slot.date}</td>
                    <td className={styles.td}>{slot.time}</td>
                    <td className={styles.td}>{slot.courts_available}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className={styles.loading}>Loading...</p>
        )}
      </div>
    );
  }

export default App;
