export async function fetchCourtAvailability(locationId) {
  const res = await fetch(`https://api-last-minute-tennis.com/scrape/location=${locationId}`);
  if (!res.ok) {
    throw new Error('Failed to fetch court availability');
  }
  return await res.json();
}