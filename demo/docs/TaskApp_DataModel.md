# Data Model
## Task Management App

### Entities

#### User
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary Key |
| email | String(120) | Unique, Not Null |
| password_hash | String(256) | Not Null |
| name | String(80) | Not Null |
| created_at | DateTime | Default: now |

#### Task
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary Key |
| title | String(200) | Not Null |
| description | Text | Nullable |
| status | Enum | Todo, In Progress, Done |
| due_date | DateTime | Nullable |
| assignee_id | UUID | Foreign Key -> User.id |
| creator_id | UUID | Foreign Key -> User.id |
| created_at | DateTime | Default: now |
| updated_at | DateTime | Auto-update |

### Relationships
- User 1:N Task (as creator)
- User 1:N Task (as assignee)

### Indexes
- Task: idx_status (status)
- Task: idx_assignee (assignee_id)
- Task: idx_due_date (due_date)
- User: idx_email (email)
