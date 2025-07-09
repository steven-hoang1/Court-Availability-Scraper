import { useState, useEffect } from 'react';
import styles from './App.module.css';
import AvailabilityTable from './components/AvailabilityTable';
import LoadingSpinner from './components/LoadingSpinner';
import { fetchCourtAvailability } from './api/fetchCourtAvailability';
import locations from './utils/Locations';
import { aggregateCourtAvailability } from './utils/AvailabilitiesAdder';

function App() {
  const [data, setData] = useState([]);
  const [locationId, setLocationId] = useState("all");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadInitialState();
  }, []);

  const loadInitialState = async () => {
    setLoading(true);
    setError('');
    try {
      const availabilityData = await fetchCourtAvailability(locationId);
      const result = aggregateCourtAvailability(availabilityData);
      setData(result.data);
    } catch (err) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Court Availabilities 🎾</h1>

      <button className={styles.refreshButton} onClick={loadInitialState}>
        Refresh Availability
      </button>

      {loading && <LoadingSpinner />}
      {error && <p className={styles.error}>Error: {error}</p>}
      
      {!loading && !error && data.length > 0 && (
        <div className={styles.tableWrapper}>
          <AvailabilityTable data={data} />
        </div>
      )}
    </div>
  );
}

export default App;