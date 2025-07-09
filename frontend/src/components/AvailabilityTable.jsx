import styles from '../styles/AvailabilityTable.module.css';

const AvailabilityTable = ({ data }) => {
  // Group by date, then by time
  const timeSet = new Set();
  const dateMap = {};

  data.forEach(({ date, time, courts_available }) => {
    if (!dateMap[date]) dateMap[date] = {};
    dateMap[date][time] = courts_available;
    timeSet.add(time);
  });

  const times = Array.from(timeSet).sort();
  const dates = Object.keys(dateMap).sort();

  return (
    <div className={styles.tableWrapper}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.th}>Time</th>
            {dates.map((date) => (
              <th key={date} className={styles.th}>{date}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {times.map((time) => (
            <tr key={time}>
              <td className={styles.td}>{time}</td>
              {dates.map((date) => (
                <td key={date} className={styles.td}>
                  {dateMap[date]?.[time] ?? '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AvailabilityTable;