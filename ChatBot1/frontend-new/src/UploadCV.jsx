import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UploadCV() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 5 * 1024 * 1024) { // 5MB limit
        setError('File size should be less than 5MB');
        return;
      }
      const fileType = selectedFile.name.split('.').pop().toLowerCase();
      if (!['pdf', 'doc', 'docx', 'txt'].includes(fileType)) {
        setError('Only PDF, DOC, DOCX, and TXT files are supported');
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/cvs/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload CV');
      }

      setSuccess('CV uploaded successfully!');
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload CV</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-input">
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx,.txt"
          />
          <p className="file-help">
            Supported formats: PDF, DOC, DOCX, TXT (max 5MB)
          </p>
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <button
          type="submit"
          className="button"
          disabled={loading || !file}
        >
          {loading ? 'Uploading...' : 'Upload CV'}
        </button>
      </form>
    </div>
  );
}

export default UploadCV;