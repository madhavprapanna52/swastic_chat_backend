
A comprehensive backend system for university student communication and collaboration

🌟 Overview
Swastik is a modern university chat platform designed exclusively for academic institutions. This backend provides secure, scalable APIs for real-time messaging, academic collaboration, quizzes, and university-specific features.

✨ Key Features
🔐 University Email Authentication (.edu/.ac.in domains)

💬 Real-time Chat Rooms & Study Groups

📚 Academic Resource Sharing

🧠 Interactive Quiz System

🏫 University-specific Communities

🔔 Smart Notifications

📱 Cross-platform APIs

🛡️ Enterprise Security (JWT, bcrypt)

🚀 Quick Start
Prerequisites
Python 3.8+

PostgreSQL 13+

Git

Installation
bash
# Clone repository
git clone https://github.com/madhavprapanna52/swastic_chat_backend.git
cd swastic_chat_backend/swastik_backend

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create database
createdb swastik_db

# Configure environment (.env file)
DATABASE_URL=postgresql://username:password@localhost/swastik_db
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
EMAIL_HOST=smtp.gmail.com
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Verify Installation
API Docs: http://localhost:8000/docs

Health Check: http://localhost:8000/health

📁 Project Structure
text
swastik_backend/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── models/                 # Database models
│   ├── schemas/               # API validation schemas
│   ├── services/             # Business logic
│   ├── utils/                # Utilities (security, database)
│   └── routes/               # API endpoints
├── requirements.txt
└── .env
🔌 API Endpoints
Authentication
POST /auth/register - Register with university email

POST /auth/login - User login

POST /auth/verify-email - Email verification

GET /auth/me - Get user profile

Chat Rooms
GET /rooms - Get user's rooms

POST /rooms - Create room

POST /rooms/{id}/join - Join room

GET /rooms/public - Browse public rooms

Messages
GET /rooms/{id}/messages - Get messages

POST /rooms/{id}/messages - Send message

PUT /messages/{id} - Edit message

Quizzes
GET /quizzes - Get available quizzes

POST /quizzes - Create quiz

POST /quizzes/{id}/attempt - Submit attempt

🧪 Testing
bash
# Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@university.edu", "password": "SecurePass123", "first_name": "John", "last_name": "Doe"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePass123"
🚀 Deployment
Docker
bash
docker build -t swastik-backend .
docker run -p 8000:8000 --env-file .env swastik-backend
Heroku
bash
heroku create swastik-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
🤝 Frontend Integration
Java Example
java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:8000/auth/login"))
    .header("Content-Type", "application/x-www-form-urlencoded")
    .POST(HttpRequest.BodyPublishers.ofString("username=demo&password=demo123"))
    .build();
JavaScript Example
javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: new URLSearchParams({username: 'demo', password: 'demo123'})
});
🔒 Security Features
JWT Authentication

Password Hashing (bcrypt)

Email Verification

University Domain Validation

Rate Limiting

Input Validation

CORS Configuration

🐛 Troubleshooting
bash
# Database issues
sudo service postgresql status
psql -U postgres -d swastik_db -c "SELECT 1;"

# Port conflicts
kill -9 $(lsof -ti:8000)

# Dependencies
pip install -r requirements.txt --force-reinstall
📊 Database Schema
users - Authentication & profiles

rooms - Chat rooms & study groups

messages - Chat content & reactions

quizzes - Quiz system

notifications - System alerts

🧪 Testing
bash
pytest                    # Run all tests
pytest --cov=app        # With coverage
pytest tests/test_auth.py # Specific tests
📞 Support
Documentation: http://localhost:8000/docs

Issues: https://github.com/madhavprapanna52/swastic_chat_backend/issues

Email: madhavprapanna52@gmail.com

📄 License
MIT License - see LICENSE file for details.

Made with ❤️ for university students by students

⭐ Star | 🐛 Issues | 💡 Features

