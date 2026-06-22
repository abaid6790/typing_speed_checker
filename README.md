# Typing Speed Tester

A modern web-based Typing Speed Tester built using Flask, HTML, CSS, JavaScript, and Supabase. The application helps users improve their typing speed while tracking performance through real-time statistics and achievements.

## Features

* Real-time WPM Calculation
* Accuracy Tracking
* Mistake Counter
* Progress Bar
* Multiple Difficulty Levels

  * Easy
  * Medium
  * Hard
* Dark / Light Theme
* Achievement System
* Anti-Paste Protection
* Auto-Finish on Paragraph Completion
* Responsive User Interface
* Random Paragraph Generation
* User Authentication with Supabase
* Session Management
* Future Support for Leaderboards and User Profiles

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database & Authentication

* Supabase

## Project Structure

```text
Typing-Speed-Tester/
│
├── app.py
├── db.py
├── .env
├── requirements.txt
├── .gitignore
│
├── data/
│   └── paragraphs.py
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── login.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   └── login.js
│   │
│   └── sounds/
│       └── success.mp3
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/typing-speed-tester.git
cd typing-speed-tester
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY
SECRET_KEY=YOUR_SECRET_KEY
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Future Enhancements

* User Profiles
* Global Leaderboard
* Typing History
* Performance Analytics
* Achievement Badges
* Export Results
* Charts and Statistics Dashboard

## Author

Abaid-ur-Rehman
