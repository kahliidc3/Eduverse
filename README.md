# EduVerse

EduVerse is a modern e-learning platform built with Django that combines interactive learning with gamification elements to create an engaging educational experience.

## Overview

EduVerse transforms traditional learning into an interactive journey by incorporating:
- Structured course content delivery
- Gamified learning experiences  
- Progress tracking and achievements
- Interactive quizzes and assessments
- Social learning features

## Features

### Core Learning Features
- **Course Management System**
  - Create and organize courses
  - Manage lessons and modules
  - Content versioning
- **Interactive Learning**
  - Rich multimedia content
  - Quiz system with multiple question types
  - Real-time progress tracking
  - Certificate generation upon completion
- **Content Organization**
  - Note-taking functionality
  - Bookmarking system
  - Search and filter capabilities

### Gamification Elements
- Achievement system with milestones
- Badge awards for accomplishments
- Points-based progression system
- Leaderboards and rankings
- Learning streaks and rewards

### User Features
- Customizable user profiles
- Course enrollment and tracking
- Personal progress dashboard
- Social certificate sharing
- Note management system

## Technical Stack

### Backend
- **Framework:** Django 4.2+
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** Django built-in auth

### Frontend
- **Framework:** HTML5/CSS3
- **Styling:** Tailwind CSS
- **JavaScript:** jQuery
- **Icons:** Font Awesome

### Additional Libraries
- Django Admin Interface
- Select2 for enhanced dropdowns
- Chart.js for analytics
- PDF generation for certificates

## Project Structure

```
eduverse/
├── core/                   # Core functionality and shared components
│   ├── middleware/        # Custom middleware
│   └── utils/            # Helper functions
├── courses/               # Course management
│   ├── models/           # Course-related models
│   └── views/            # Course views
├── gamification/          # Gamification features
│   ├── achievements/     # Achievement system
│   └── rewards/         # Points and badges
├── users/                # User management
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # User-uploaded content
├── templates/            # HTML templates
└── eduverse/            # Project settings
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eduverse.git
cd eduverse
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin interface at `http://localhost:8000/admin`
2. Create courses and content through the admin panel
3. Register new users through the registration page
4. Enroll in courses and start learning

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

For support or inquiries:
- Email: support@eduverse.com
- Website: https://eduverse.com
- Documentation: https://docs.eduverse.com

## License

This project is private and confidential. All rights reserved.