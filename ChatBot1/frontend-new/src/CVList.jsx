import React, { useEffect, useState } from 'react';

function CVList() {
  const [cvs, setCvs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchCVs = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/cvs/`);
      if (!response.ok) {
        throw new Error('Failed to fetch CVs');
      }
      const data = await response.json();
      setCvs(data.results || data);
    } catch (err) {
      setError('Failed to load CVs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCVs();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/cvs/${id}/`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete CV');
      }

      setSuccess('CV deleted successfully');
      setCvs(cvs.filter(cv => cv.id !== id));
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess('');
      }, 3000);
    } catch (err) {
      setError('Failed to delete CV');
      
      // Clear error message after 3 seconds
      setTimeout(() => {
        setError('');
      }, 3000);
    }
  };

  if (loading) {
    return <div className="loading">Loading CVs...</div>;
  }

  return (
    <div className="cv-list">
      <h2>Uploaded CVs</h2>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {cvs.length === 0 ? (
        <p>No CVs uploaded yet. Go to Upload CV to add one.</p>
      ) : (
        <ul className="cv-items">
          {cvs.map(cv => (
            <li key={cv.id} className="cv-item">
              <div className="cv-info">
                <span className="cv-name">CV #{cv.id}</span>
                <span className="cv-date">
                  {new Date(cv.uploaded_at).toLocaleDateString()}
                </span>
              </div>
              <div className="cv-actions">
                <a
                  href={cv.file}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="button"
                >
                  View
                </a>
                <button
                  onClick={() => handleDelete(cv.id)}
                  className="button delete"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default CVList;