import { useState, useEffect } from 'react';
import styles from './App.module.css';
import AvailabilityTable from './components/AvailabilityTable';
import LoadingSpinner from './components/LoadingSpinner';
import { fetchCourtAvailability } from './api/fetchCourtAvailability';

function App() {
  const [data, setData] = useState([]);
  const [locationId, setLocationId] = useState(2); // could be controlled by a dropdown later
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await fetchCourtAvailability(locationId);
      setData(result);
    } catch (err) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Surry Hills Court Availability 🎾</h1>

      <button className={styles.refreshButton} onClick={loadData}>
        Refresh Availability
      </button>

      {loading && <LoadingSpinner />}
      {error && <p className={styles.error}>Error: {error}</p>}
      {!loading && !error && data.length > 0 && <AvailabilityTable data={data} />}
    </div>
  );
}

export default App;