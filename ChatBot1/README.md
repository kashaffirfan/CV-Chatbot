# CV Chatbot Application

A full-stack application that allows users to upload CVs and chat with an AI about the content of those CVs. Built with Django (backend) and React (frontend).

## Features

- Upload CV files (PDF, DOC, DOCX, TXT)
- View and manage uploaded CVs
- Chat interface to ask questions about the CVs
- Real-time AI responses based on CV content
- Modern and responsive UI

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- pip (Python package manager)
- npm (Node package manager)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

The backend will be running at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory with:
   ```
   VITE_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be running at `http://localhost:5173`

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Use the "Upload CV" page to upload CV files
3. View and manage your CVs on the home page
4. Use the chat interface to ask questions about the uploaded CVs

## File Format Support

- PDF (.pdf)
- Microsoft Word (.doc, .docx)
- Text files (.txt)

## Technical Details

### Backend
- Django REST Framework for API
- SQLite database
- PDF and DOC file processing
- AI-powered text analysis and question answering

### Frontend
- React with Vite
- Modern UI components
- Real-time chat interface
- Responsive design

## Notes

- Maximum file size: 5MB
- Supported file formats: PDF, DOC, DOCX, TXT
- The AI model needs at least one CV uploaded to answer questions
- For development purposes only - additional security measures needed for production 