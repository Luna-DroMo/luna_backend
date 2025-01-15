# Luna Backend Technical Documentation

## Project Overview

Luna is the web implementation of the research study titled "Forecasting Intra-individual Changes of Affective States Taking into Account Inter-individual Differences Using Intensive Longitudinal Data from a University Student Dropout Study in Mathematics" conducted by Augustin Kelava, Pascal Kilian, Judith Glässer, Samuel Merk, and Holger Brandt at the University of Tübingen. The goal of this web application is to understand and forecast student dropout in German universities using state-of-the-art psychometric methods. Web app backend is a Django-based backend application designed to manage university-related operations, including student management, module handling, and survey systems.

## Technical Requirements

### Core Requirements

- Python 3.9
- Django 4.2.5
- PostgreSQL Database
- Docker & Docker Compose

### Key Dependencies

- Django Rest Framework 3.14.0 (API Framework)
- django-cors-headers 4.2.0 (CORS handling)
- psycopg2-binary 2.9.7 (PostgreSQL adapter)
- django-cron (Scheduled tasks)
- drf_yasg (API Documentation)
- python-decouple (Environment configuration)

## Project Structure

```
luna_backend/
├── luna/                   # Main application directory
│   ├── api/               # API endpoints and views
│   ├── core/              # Core functionality and models
│   ├── modelling/         # Data modeling and analysis
│   └── luna/              # Project settings and configuration
├── documentation/         # Project documentation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Docker services configuration
└── entrypoint.sh         # Docker entrypoint script
```

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`
4. Run migrations: `python manage.py migrate`
5. Start development server: `python manage.py runserver`

## Docker Deployment

The application can be deployed using Docker:

```bash
docker-compose up --build
```

## Admin Portal

The application provides a Django admin interface for administrative tasks:

### Access

- URL: `/admin`
- Login with superuser credentials
- Accessible only to users with admin privileges
