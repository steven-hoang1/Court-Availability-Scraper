export async function fetchCourtAvailability(locationId) {
    try {
        const res = await fetch(`https://api-last-minute-tennis.com/location/${locationId}`);
        return await res.json();
    } catch (err) {
    console.error('Caught fetch error:', err);
    throw err;
    }
}