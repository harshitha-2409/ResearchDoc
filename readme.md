# ResearchDoc

ResearchDoc is an AI-powered research management platform built using Django. The system allows users to organise research projects, upload academic resources, generate AI summaries, create APA citations, compare research papers, and manage research workflows through a modern SaaS-style dashboard.

---

# Live Deployment

Deployed Application:

[https://researchdoc-zzgc.onrender.com](https://researchdoc-zzgc.onrender.com)

GitHub Repository:

[https://github.com/harshitha-2409/ResearchDoc](https://github.com/harshitha-2409/ResearchDoc)

---

# Features

## User Authentication

* User registration
* User login/logout
* Secure user-specific dashboards
* Multi-user project isolation

## Project Management

* Create projects
* Edit projects
* Archive projects
* Restore archived projects
* Dashboard project management

## Research Resource Management

* Upload PDF research papers
* Store external research links
* Add authors and publication year
* Add abstract information
* Delete resources
* Edit resources

## AI Features

* AI-generated research summaries
* Key findings generation
* Citation generation
* AI research comparison generation
* Structured comparison table interface

## Research Comparison System

* Create comparison entries
* Edit comparisons
* Delete comparisons
* Table-based research comparison UI

## Summary Management

* Edit AI summaries
* Delete summaries
* Citation editing
* Key findings editing

## Search & Organisation

* Resource tagging system
* Search functionality
* Dashboard analytics

## UI/UX Features

* Responsive design
* Modern dashboard layout
* SaaS-style interface
* Card-based UI
* Comparison tables
* Archive workflow

## Deployment

* GitHub integration
* Render cloud deployment
* Production static file handling
* Environment variable configuration

---

# Technology Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Django     | Backend framework         |
| Python     | Core programming language |
| SQLite     | Database                  |
| HTML/CSS   | Frontend development      |
| Render     | Cloud deployment          |
| GitHub     | Version control           |
| OpenAI API | AI summary generation     |
| WhiteNoise | Static file hosting       |
| Gunicorn   | Production server         |

---

# Database Models

## Project

Stores user research workspaces.

## Resource

Stores uploaded research papers and external research links.

## Summary

Stores AI-generated research summaries and citations.

## Comparison

Stores AI-generated research comparisons.

## Tag

Stores resource tags for categorisation.

## ResourceTag

Handles many-to-many relationships between resources and tags.

## ComparisonItem

Stores structured comparison criteria and notes.

---

# System Architecture

The application follows a standard Django MVC/MVT architecture.

## Frontend

* HTML templates
* CSS styling
* Django template rendering

## Backend

* Django views
* URL routing
* Authentication system
* AI processing logic
* CRUD operations

## Database Layer

* Django ORM
* SQLite relational database
* Model relationships

## Deployment Layer

* Render cloud hosting
* Gunicorn production server
* WhiteNoise static file serving

---

# CRUD Operations Implemented

| Module      | Create | Read | Update | Delete/Archive |
| ----------- | ------ | ---- | ------ | -------------- |
| Projects    | Yes    | Yes  | Yes    | Archive        |
| Resources   | Yes    | Yes  | Yes    | Yes            |
| Summaries   | Yes    | Yes  | Yes    | Yes            |
| Comparisons | Yes    | Yes  | Yes    | Yes            |

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/harshitha-2409/ResearchDoc.git
cd ResearchDoc
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
LLM_API_KEY=your-openai-api-key
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Start Server

```bash
python manage.py runserver
```

---

# Deployment Process

The application was deployed using Render.

## Deployment Steps

1. Push project to GitHub
2. Connect GitHub repository to Render
3. Configure environment variables
4. Configure build/start commands
5. Deploy application

## Production Configuration

### Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command

```bash
gunicorn researchdoc.wsgi:application
```

---

# Future Improvements

* Advanced semantic search
* PDF text extraction improvements
* AI citation validation
* Research recommendation engine
* Collaborative project sharing
* Export to BibTeX
* Research analytics dashboard
* Improved mobile responsiveness

---

# Challenges Faced

* Django deployment configuration
* Static file management
* Environment variable handling
* AI integration setup
* CRUD workflow integration
* URL routing conflicts
* Production deployment debugging

---

# Learning Outcomes

This project helped develop practical skills in:

* Full-stack web development
* Django architecture
* Database modelling
* SaaS application development
* Authentication systems
* Cloud deployment
* Git and GitHub workflows
* AI integration
* Debugging and troubleshooting

---

# AI Usage Acknowledgement

AI tools were used to support development, debugging assistance, UI refinement, deployment troubleshooting, and implementation guidance throughout the project. Final integration, testing, architecture decisions, and customisation were completed manually as part of the development process.

---

# Author

Harshitha P

Master of Computer Science Management

The University of Queensland

---

# License

This project was developed for academic purpose only.