# FlashLearn – Flashcard Revision Platform

## Overview
FlashLearn is a full-stack web application built using Django that allows users to create, manage, and study flashcards through interactive revision tools such as flashcards, quizzes, and analytics tracking. The system is designed to support active recall and spaced repetition learning techniques.

---

## Features
- User authentication (login/register/logout via Django AllAuth)
- Create, edit, and delete flashcard decks
- Add and manage flashcards within decks
- Interactive flashcard flipping system
- Multiple-choice and written-answer quiz modes
- Automated score tracking and storage in database
- Analytics dashboard with performance graphs (Chart.js)
- Overview page showing:
  - Cards studied
  - Accuracy percentage
  - Study streak
- Dark / Light mode UI toggle
- Responsive and consistent UI design

---

## Technologies Used
- Python 3
- Django
- HTML5
- CSS3
- JavaScript
- Chart.js
- SQLite (development database)

---

## Installation & Setup

### 1. Clone the repository
git clone <repository-url>
cd project

### 2. Create virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

---

### 3. Install dependencies
pip install -r requirements.txt

---

### 4. Run migrations
python manage.py makemigrations
python manage.py migrate

---

### 5. Create superuser (optional)
python manage.py createsuperuser

---

### 6. Run server
python manage.py runserver

Open:
http://127.0.0.1:8000/

---

## Usage

1. Register / log in
2. Go to My Decks
3. Create or manage decks
4. Add flashcards
5. Study using flashcards (active recall)
6. Take quizzes (MCQ or written)
7. View analytics dashboard
8. Track progress on overview page

---

## Project Structure

```text
project/
├── app/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── db.sqlite3
└── requirements.txt

---

## Notes
- Quiz results are stored in the database and used for analytics
- Streak and accuracy are calculated dynamically
- Decks and cards must exist before studying
- Run migrations before starting the server

---

## Demo
A full demonstration video of the system is included in the project submission.

---
