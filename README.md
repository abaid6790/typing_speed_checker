# AI-Powered Typing Speed Tester & Productivity Platform

A full-stack typing speed tester and productivity platform built using Flask, Supabase, HTML, CSS, JavaScript, and Chart.js.

The application helps users improve typing speed and accuracy while tracking performance through analytics, achievements, leaderboards, and gamification features.

---

## Features

### Authentication
- User Registration
- User Login
- User Logout
- Secure Session Management
- Protected Routes

### Typing Test
- Real-Time Typing Speed (WPM)
- Real-Time Accuracy Calculation
- Mistake Tracking
- Easy, Medium, Hard Difficulty Levels
- Multiple Test Durations
- Random Paragraph Generation
- Auto Start Timer
- Auto Finish Test
- Restart Test

### Dashboard
- User Statistics Overview
- Best WPM
- Average WPM
- Total Tests
- Total XP
- Level Tracking
- Streak Tracking

### Analytics
- WPM Trend Charts
- Accuracy Trend Charts
- Progress Visualization
- Performance Analytics using Chart.js

### Gamification
- XP Reward System
- Level System
- Achievement System
- Badge Unlocking
- Daily Streak Tracking

### Leaderboard
- Global Ranking
- Best WPM Ranking
- XP Ranking
- Level Ranking

### Profile Management
- User Profile Page
- Update Profile Information
- Track Progress and Achievements

### Database Integration
- Supabase PostgreSQL Database
- Secure Data Storage
- Real-Time User Statistics

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### Database
- Supabase
- PostgreSQL

### Deployment
- Render
- Railway
- GitHub

---

## Project Structure

```text
typing-speed-platform/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── database/
│   └── supabase.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── typing.py
│   ├── history.py
│   ├── analytics.py
│   ├── achievements.py
│   ├── leaderboard.py
│   └── profile.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── typing_test.html
│   ├── history.html
│   ├── analytics.html
│   ├── achievements.html
│   ├── leaderboard.html
│   └── profile.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── profile.css
│   │
│   └── js/
│       └── typing.js
│
├── utils/
│   └── achievements.py
│
└── data/
    ├── easy.py
    ├── medium.py
    └── hard.py
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/typing-speed-platform.git
cd typing-speed-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
```

---

## Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

- AI Typing Coach
- PDF Certificates
- CSV/Excel Export
- Email Verification
- Forgot Password System
- Daily Challenges
- Weekly Challenges
- Public User Profiles

---
---

## Technologies Used

Python, Flask, Supabase, PostgreSQL, HTML5, CSS3, JavaScript, Chart.js