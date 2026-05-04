# High-Level Design (HLD)
## Task Management App

### 1. System Overview
A Flask-based web application with PostgreSQL database, following MVC pattern.

### 2. Architecture Layers
- **Presentation Layer**: HTML/CSS/JS frontend with Jinja2 templates
- **Application Layer**: Flask routes and controllers
- **Business Layer**: Service classes for task and user management
- **Data Layer**: SQLAlchemy ORM with PostgreSQL

### 3. Key Components
| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | Flask | HTTP routing, request handling |
| ORM | SQLAlchemy | Database abstraction |
| Auth | Flask-Login | Session management |
| Frontend | Bootstrap 5 | Responsive UI |
| Database | PostgreSQL | Data persistence |

### 4. API Design
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/tasks | GET | List all tasks |
| /api/tasks | POST | Create new task |
| /api/tasks/:id | GET | Get task details |
| /api/tasks/:id | PUT | Update task |
| /api/tasks/:id | DELETE | Delete task |
| /api/auth/login | POST | User login |
| /api/auth/register | POST | User registration |

### 5. Authentication Flow
1. User submits credentials
2. Server validates against database
3. Session created with Flask-Login
4. Cookie set for subsequent requests
