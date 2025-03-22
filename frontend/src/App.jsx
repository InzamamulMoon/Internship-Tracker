import { useState, useEffect } from 'react'
import './App.css'
import mockInternships from "./mockData"; // Import mock data

function App() {
  const [internships, setInternships] = useState([]);

  useEffect(() => {
    // Simulate fetching from a backend API
    setInternships(mockInternships);
  }, []);

return (
  <div>
    <h1>Internship Tracker</h1>
    <ul>
      {internships.length > 0 ? (
        internships.map((internship) => (
          <li key={internship.id}>
            {internship.company} - {internship.role} ({internship.location}) <a href={internship.link} target="_blank" rel="noopener noreferrer">
              Apply Here
            </a>
          </li>
        ))
      ) : (
        <p>No internships found.</p>
      )}
    </ul>
  </div>
);

}

export default App;
