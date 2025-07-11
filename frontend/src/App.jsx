import { useState, useEffect } from 'react';
import styles from './App.module.css';
import AvailabilityTable from './components/AvailabilityTable';
import LoadingSpinner from './components/LoadingSpinner';
import { fetchCourtAvailability } from './api/fetchCourtAvailability';
import locations from './utils/Locations';
import { aggregateCourtAvailability } from './utils/AvailabilitiesAdder';
import { Flex } from "@chakra-ui/react"

function App() {
  const [data, setData] = useState([]);
  const [locationId, setLocationId] = useState(2);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (locId = locationId) => {
    setLoading(true);
    setError('');
    try {
      const availabilityData = await fetchCourtAvailability(locId);
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
      <Flex className={styles.locationSelector} gap="5" direction="row">
        <label htmlFor="location-select" className={styles.label}>
          Select Location:
        </label>
        <select
          id="location-select"
          value={locationId}
          onChange={(e) => {
            const newLocationId = e.target.value;
            console.log(newLocationId)
            setLocationId(newLocationId);
            loadData(newLocationId);
          }}
          className={styles.select}
        >
          {locations.map((location) => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>
        <button className={styles.refreshButton} onClick={() => loadData(locationId)} >
        Refresh
      </button>
      </Flex>
      {loading && <LoadingSpinner />}
      {error && <p className={styles.error}>Error: {error}</p>}
      
      {!loading && !error && data.length > 0 && (
        <div className={styles.tableWrapper}>
          <AvailabilityTable data={data} />
        </div>
      )}
      <div className={styles.supportSection}>
        <h2 className={styles.supportHeading}>Enjoying the service?</h2>
        <p className={styles.supportText}>
          If you find this helpful, consider supporting us:
        </p>
        <div className={styles.supportLinks}>
          <a
            href="https://buymeacoffee.com/lastminutetennis"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.supportButton}
          >
            ☕ Buy Me a Coffee
          </a>
          <a
            href="https://amzn.to/46zH1Fj"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.supportButton}
          >
            🎾 Use our Link to Buy Tennis Balls
          </a>
        </div>
      </div>
    </div>
  );
}

export default App;