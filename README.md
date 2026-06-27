# 🚀 AI Typing Speed Tester

A modern Typing Speed Test platform built with **Flask** and **Supabase** featuring authentication, leaderboards, achievements, challenges, analytics, profiles, and gamification.

---

## ✨ Features

### 👤 Authentication
- User Registration
- Secure Login
- Logout
- Email Verification (Supabase)
- Forgot Password
- Reset Password

---

### ⌨ Typing Test

- Easy / Medium / Hard Modes
- 30 / 60 / 120 Second Tests
- Live WPM Calculation
- Live Accuracy
- Mistake Counter
- XP Reward System
- Automatic Result Saving

---

### 📊 Dashboard

- Total Tests
- Best WPM
- Average WPM
- Highest Accuracy
- Total XP
- Current Level
- Current Streak

---

### 📈 Analytics

- WPM History
- Accuracy History
- Progress Charts
- Performance Tracking

---

### 🏆 Leaderboard

- Highest WPM Rankings
- Top XP Rankings
- User Levels

---

### 🎖 Achievements

Unlock achievements automatically:

- First Test
- Speed Beginner
- Speed Master
- Accuracy Expert
- Consistent Typer
- XP Collector

---

### 🎯 Challenges

Daily Challenges

- Complete Tests
- Reach Target WPM
- Reach Target Accuracy

Weekly Challenges

- Complete Multiple Tests
- Earn XP
- Improve Speed

Challenge Progress updates automatically.

---

### 👤 Profile

- Full Name
- Bio
- Country
- Avatar
- Public Profile
- Edit Profile

---

### 🌐 Public Profile

Every user has a public profile.

Shows

- Name
- Level
- XP
- Best WPM
- Accuracy
- Total Tests
- Achievements

---

### 🔐 Security

- Password Hashing (Supabase)
- Email Verification
- Password Reset
- Session Authentication
- Protected Routes
- Disabled Copy/Paste During Test

---

## 🛠 Tech Stack

Backend

- Flask
- Python

Frontend

- HTML
- CSS
- JavaScript

Database

- Supabase PostgreSQL

Authentication

- Supabase Auth

Charts

- Chart.js

Deployment Ready

- Render
- Railway
- Vercel (Frontend)
- Supabase

---

## 📁 Project Structure

```
Typing-Speed-Tester/

│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── routes/
├── templates/
├── static/
├── database/
├── utils/
├── data/
└── README.md
```

---

## ⚙ Installation

Clone repository

```bash
git clone https://github.com/yourusername/Typing-Speed-Tester.git
```

Install packages

```bash
pip install -r requirements.txt
```

Create

```
.env
```

Add

```env
SUPABASE_URL=your_url

SUPABASE_KEY=your_key

SECRET_KEY=your_secret
```

Run

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

## 📸 Screens

- Login
- Register
- Dashboard
- Typing Test
- Analytics
- Achievements
- Challenges
- Leaderboard
- Profile
- Public Profile

(Add screenshots after pushing to GitHub.)

---

## 🚀 Future Improvements

- Multiplayer Mode
- AI Typing Coach

---

## 👨‍💻 Author
Abaid-ur-Rehman