export async function fetchCourtAvailability(locationId) {
    try {
        const res = await fetch(`http://localhost:10000/location/${locationId}`);
        return await res.json();
    } catch (err) {
    console.error('Caught fetch error:', err);
    throw err;
    }
}