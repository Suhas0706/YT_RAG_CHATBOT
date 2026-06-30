A full-stack web application that allows users to process YouTube videos and ask questions about their content using Retrieval-Augmented Generation (RAG) technology.

🚀 Features
YouTube Video Processing: Extract and process transcripts from YouTube videos
Intelligent Q&A: Ask questions about video content and get AI-powered answers
FastAPI Backend: Robust Python backend with FastAPI framework
React Frontend: Modern, responsive user interface built with React and Vite
Vector Search: FAISS-powered semantic search for relevant content retrieval
OpenAI Integration: Leverages GPT models for natural language responses
🛠️ Tech Stack
Backend
Python - Core programming language
FastAPI - Modern, fast web framework for building APIs
FAISS - Efficient similarity search and clustering of dense vectors
OpenAI API - For natural language processing and generation
YouTube Transcript API - Extract transcripts from YouTube videos
Uvicorn - ASGI web server implementation for Python
Frontend
React - JavaScript library for building user interfaces
Vite - Fast build tool and development server
Tailwind CSS - Utility-first CSS framework
Axios - HTTP client for making API requests
📋 Prerequisites
Before running this application, make sure you have the following installed:

Python 3.8+
Node.js 16+
npm or yarn
OpenAI API Key (for AI functionality)
🔧 Installation
Backend Setup
Navigate to the backend directory:

cd backend
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On Windows:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate
Install Python dependencies:

pip install -r requirements.txt
Create a .env file in the backend directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here
Frontend Setup
Navigate to the frontend directory:

cd frontend
Install Node.js dependencies:

npm install
🚀 Usage
Running the Application
Start the Backend Server:

cd backend
uvicorn main:app --reload
The backend will be available at http://localhost:8000

Start the Frontend Development Server:

cd frontend
npm run dev
The frontend will be available at http://localhost:5173

How to Use
Process a Video:

Enter a YouTube video URL in the input field
Click "Process Video" to extract and index the transcript
Ask Questions:

Once the video is processed, enter your question in the chat input
The AI will provide answers based on the video content
📡 API Endpoints
Backend API
POST /process_video - Process a YouTube video URL

Request body: {"url": "https://www.youtube.com/watch?v=VIDEO_ID"}
Response: Success/error message
POST /ask - Ask a question about the processed video

Request body: {"question": "Your question here"}
Response: AI-generated answer
Note: Make sure to keep your OpenAI API key secure and never commit it to version control.
