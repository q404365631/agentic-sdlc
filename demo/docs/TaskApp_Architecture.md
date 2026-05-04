# Architecture Document
## Task Management App

### Tech Stack
- **Backend**: Python 3.11 + Flask 3.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 + Flask-SQLAlchemy
- **Auth**: Flask-Login + Werkzeug security
- **Frontend**: Bootstrap 5 + vanilla JS
- **Templates**: Jinja2

### Project Structure
```
demo/src/
├── app.py              # Flask application factory
├── config.py           # Configuration (dev, test, prod)
├── models/
│   ├── __init__.py
│   ├── user.py         # User model
│   └── task.py         # Task model
├── routes/
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   └── tasks.py        # Task CRUD routes
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── task_service.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── task_form.html
└── static/
    ├── css/style.css
    └── js/app.js
```

### Key Design Decisions
1. **Soft Delete**: Tasks are soft-deleted for recovery
2. **Status Enum**: Three states only (Todo, In Progress, Done)
3. **UUID Primary Keys**: Better for distributed systems
4. **Service Layer**: Business logic separated from routes
