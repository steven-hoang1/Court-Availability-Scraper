export function aggregateCourtAvailability(data) {
  const isArray = Array.isArray(data);
  const dataArray = isArray ? data : [data];
    if (dataArray.length === 1) 
        return {
        location_id: 0,
        data: dataArray[0].data,
        }; 

  const aggregationMap = new Map();
  data.forEach(({ data: slots }) => {
    slots.forEach(({ date, time, courts_available }) => {
      const key = `${date}|${time}`;
      const current = aggregationMap.get(key) || 0;
      aggregationMap.set(key, current + courts_available);
    });
  });

  // Transform the map back into the desired format
  const aggregatedData = Array.from(aggregationMap.entries()).map(
    ([key, courts_available]) => {
      const [date, time] = key.split('|');
      return { date, time, courts_available };
    }
  );

  return { location_id: 0, data: aggregatedData };
}