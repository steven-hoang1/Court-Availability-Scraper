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
      <div className="min-h-screen bg-blue-50 flex flex-col items-center py-10">
        <h1 className="text-4xl text-blue-700 font-bold mb-8">Surry Hills</h1>
        {data ? (
          <div className="overflow-x-auto w-full max-w-2xl shadow-lg rounded-lg bg-white">
            <table className="min-w-full divide-y divide-blue-200">
              <thead className="bg-blue-100">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Time</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Courts Available</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-blue-100">
                {data.map((slot, idx) => (
                  <tr key={idx} className="hover:bg-blue-50 transition">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{slot.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{slot.time}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-blue-600">{slot.courts_available}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-blue-700 text-lg mt-8">Loading...</p>
        )}
      </div>
    );  
  }

export default App;
