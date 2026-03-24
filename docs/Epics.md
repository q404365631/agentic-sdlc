# Product Epics
# MVP Appointment Booking Application

## Document Information
| **Version** | **Date** | **Author** | **Status** |
|-------------|----------|------------|------------|
| 1.0         | 2026-03-24 | AI Planning Agent | Draft |

**Related Documents:**
- [Business Requirements Document (BRD)](./BRD.md)
- [Features Document](./Features.md)

## What Are Epics?
Epics are large bodies of work that can be broken down into smaller, manageable features and user stories. Each epic represents a high-level capability or theme that delivers value to users and aligns with business objectives defined in the BRD.

## Epic Overview
This document defines 5 core epics for the MVP Appointment Booking Application:

| **Epic ID** | **Epic Name** | **Priority** | **Business Value** |
|-------------|---------------|--------------|-------------------|
| EP-001 | User Authentication & Account Management | Must Have | Enables secure user access and personalization |
| EP-002 | Doctor Discovery & Search | Must Have | Core capability for patients to find providers |
| EP-003 | Appointment Booking System | Must Have | Primary revenue-generating functionality |
| EP-004 | Appointment Management | Must Have | Enables users to track and manage bookings |
| EP-005 | Provider Administration | Must Have | Enables administrative control of doctors and availability |

---

## EP-001: User Authentication & Account Management

### Epic Statement
**As a** patient
**I want to** create and manage my account securely
**So that** I can access the appointment booking system with my personal information saved for quick bookings.

### Business Objective
- Enable secure access to the platform
- Reduce friction in repeat bookings through saved user profiles
- Build user database for future engagement and analytics

### Success Metrics
- 90% successful registration completion rate
- <2 minutes average registration time
- <5% forgotten password requests per month
- Zero unauthorized account access incidents

### User Personas
**Primary:**
- New patients seeking healthcare appointments
- Returning patients accessing their booking history

**Secondary:**
- Practice staff assisting patients with account issues

### Scope & Boundaries
**In Scope:**
- User registration with email/password
- Secure login and logout
- Password strength validation
- Session management
- Basic profile information (name, email, phone)

**Out of Scope (Deferred):**
- Social login (Google, Facebook)
- Two-factor authentication (2FA)
- Password reset via email (manual reset for MVP)
- Profile photo upload
- Multi-language preferences
- Notification preferences

### Dependencies
- Email service provider for account verification
- Secure password hashing library (bcrypt)
- SSL certificate for HTTPS

### Risks & Mitigation
| **Risk** | **Mitigation** |
|----------|----------------|
| Weak passwords compromise security | Enforce strong password policy (8+ chars, numbers, special chars) |
| Session hijacking | Implement secure session management with httpOnly cookies |
| Account enumeration attacks | Generic error messages, rate limiting on login attempts |

### Acceptance Criteria (Epic-Level)
- [ ] Users can register with valid email and strong password
- [ ] Users can log in with correct credentials
- [ ] Users remain logged in across browser sessions (7 days)
- [ ] Users can log out successfully
- [ ] Invalid credentials show appropriate error messages
- [ ] Passwords are stored encrypted (never plain text)
- [ ] Session expires after 7 days of inactivity

### Technical Considerations
- Use bcrypt for password hashing (cost factor: 12)
- Implement JWT or secure session cookies
- HTTPS required for all authentication endpoints
- Rate limiting: 5 failed login attempts = 15-minute lockout

---

## EP-002: Doctor Discovery & Search

### Epic Statement
**As a** patient
**I want to** search and discover doctors by specialty and availability
**So that** I can find the right healthcare provider for my needs quickly.

### Business Objective
- Enable efficient provider discovery
- Reduce phone inquiries about doctor availability
- Improve patient experience with self-service search
- Support practice growth by showcasing all providers

### Success Metrics
- <3 seconds average search response time
- 85% of searches result in viewing at least one doctor profile
- 60% of doctor profile views lead to booking attempt
- 70% user satisfaction with search functionality

### User Personas
**Primary:**
- Patients searching for specific specialist (e.g., dermatologist)
- Patients looking for any available doctor in timeframe
- New patients unfamiliar with practice providers

**Secondary:**
- Practice staff helping patients find suitable doctors

### Scope & Boundaries
**In Scope:**
- Search doctors by name (partial match, case-insensitive)
- Filter by specialty category
- Filter by available date
- Display doctor profiles (name, specialty, bio, photo)
- Show real-time availability indicator
- Responsive grid/list view of search results

**Out of Scope (Deferred):**
- Advanced filters (gender, language spoken, years of experience)
- Location-based search (distance from patient)
- Sort by rating/reviews
- Availability preview in search results (requires profile view)
- Save favorite doctors
- Doctor comparison side-by-side
- Map view of doctor locations

### Dependencies
- Doctor profiles populated in database
- Specialty taxonomy defined
- Doctor availability schedules configured
- Profile photos/placeholders available

### Risks & Mitigation
| **Risk** | **Mitigation** |
|----------|----------------|
| Slow search performance with many doctors | Implement database indexing on name and specialty fields |
| No search results (poor UX) | Provide helpful message, suggest browsing all doctors |
| Outdated availability information | Real-time availability check when viewing profile |

### Acceptance Criteria (Epic-Level)
- [ ] Users can search by doctor name (minimum 2 characters)
- [ ] Search returns relevant results within 2 seconds
- [ ] Users can filter by specialty from dropdown
- [ ] Users can filter by available date (date picker)
- [ ] Search results display doctor name, specialty, and photo
- [ ] "View Profile" button on each doctor card
- [ ] Empty search state shows friendly message
- [ ] Search results are mobile-responsive

### Technical Considerations
- Database indexing on `doctors.name` and `doctors.specialty`
- Use SQL `LIKE` or full-text search for name matching
- Join query to check availability when filtering by date
- Pagination for >50 results (display 20 per page)
- Debounce search input (300ms) to reduce API calls

---

## EP-003: Appointment Booking System

### Epic Statement
**As a** patient
**I want to** view available time slots and book an appointment with my chosen doctor
**So that** I can secure a healthcare appointment at a convenient time without making phone calls.

### Business Objective
- Automate appointment scheduling to reduce staff workload
- Enable 24/7 booking capability
- Prevent double-booking through system validation
- Increase appointment conversion rate by 25%
- Generate appointment data for analytics and reporting

### Success Metrics
- 80% booking completion rate (users who start booking process)
- <3 minutes average time to complete booking
- Zero double-booking incidents
- 100% booking confirmation accuracy
- 95% user satisfaction with booking process

### User Personas
**Primary:**
- Patients booking first appointment with new doctor
- Existing patients scheduling follow-up appointments
- Caregivers booking on behalf of family members

**Secondary:**
- Practice staff monitoring booking activity

### Scope & Boundaries
**In Scope:**
- View doctor's availability calendar (next 30 days)
- Display available time slots (30-minute intervals)
- Select date and time slot
- Confirm booking with review screen
- Prevent double-booking (database constraint + locking)
- Generate unique booking ID
- Display booking confirmation on-screen
- Send confirmation email with appointment details
- Booking available only to logged-in users

**Out of Scope (Deferred):**
- Same-day appointment booking
- Recurring appointment booking
- Booking multiple appointments at once
- Preferred time zone selection
- SMS confirmation
- Add to calendar (Google, Outlook) integration
- Booking for multiple family members
- Telehealth vs. in-person selection
- Reason for visit / chief complaint collection
- Insurance information collection
- Payment/deposit at booking

### Dependencies
- User authentication system (EP-001)
- Doctor profiles and availability configured (EP-005)
- Email service provider integration
- Database with transaction support (SQLite with WAL mode)

### Risks & Mitigation
| **Risk** | **Mitigation** |
|----------|----------------|
| Race condition: two users book same slot | Implement pessimistic locking or unique constraint at database level |
| User abandons booking mid-process | Track abandonment analytics, optimize checkout flow, no slot held until confirmed |
| Email delivery failure | Store booking in database first, retry email delivery asynchronously |
| Timezone confusion | Display timezone clearly, use single timezone for MVP (practice local) |

### Acceptance Criteria (Epic-Level)
- [ ] Calendar view displays available slots for selected doctor
- [ ] Past dates and unavailable slots are not selectable
- [ ] User selects date and sees available time slots for that day
- [ ] User clicks time slot and proceeds to confirmation screen
- [ ] Confirmation screen shows: doctor, date, time, patient name
- [ ] User confirms booking (one-click)
- [ ] System validates slot still available (race condition check)
- [ ] Booking saved to database with "Confirmed" status
- [ ] Unique booking ID generated (e.g., BK-20260324-0001)
- [ ] Confirmation shown on-screen with all details
- [ ] Confirmation email sent to patient within 1 minute
- [ ] Booked slot immediately unavailable to other users
- [ ] Booking appears in patient's "My Appointments" list

### Technical Considerations
- Use calendar library (FullCalendar, React Big Calendar, or custom)
- Implement optimistic UI with loading states
- Database transaction for booking with ACID properties
- Unique constraint on (doctor_id, appointment_date, start_time)
- Use database-level locking: `SELECT ... FOR UPDATE`
- Email queuing system for reliability (RabbitMQ or database queue)
- Generate slots dynamically based on doctor availability rules
- Handle edge cases: end of month, holidays (blocked by admin)

---

## EP-004: Appointment Management

### Epic Statement
**As a** patient
**I want to** view my scheduled and past appointments and cancel if needed
**So that** I can keep track of my healthcare appointments and adjust my schedule when necessary.

### Business Objective
- Reduce phone calls for appointment inquiries
- Enable self-service appointment cancellation
- Improve patient satisfaction with transparency
- Free up cancelled slots for other patients immediately
- Reduce no-shows through better appointment visibility

### Success Metrics
- 90% of users access "My Appointments" at least once
- 100% cancellation accuracy (slot released immediately)
- 30% reduction in phone calls for appointment status inquiries
- <1% cancellation errors or disputes

### User Personas
**Primary:**
- Patients managing their own appointments
- Patients who need to reschedule or cancel

**Secondary:**
- Practice staff handling patient inquiries

### Scope & Boundaries
**In Scope:**
- View list of upcoming appointments (chronological order)
- View list of past appointments (completed/cancelled)
- Display appointment details: doctor, specialty, date, time, status, booking ID
- Cancel upcoming appointments (with 24-hour restriction)
- Confirmation prompt before cancellation
- Cancelled appointments show "Cancelled" status
- Email confirmation of cancellation

**Out of Scope (Deferred):**
- Reschedule appointment (must cancel and re-book)
- Edit appointment details
- Add appointment reminders
- Export appointments to calendar
- Print appointment details
- Share appointment details
- Appointment history beyond 1 year
- Bulk cancellation

### Dependencies
- Appointment booking system (EP-003)
- User authentication (EP-001)
- Email service for cancellation confirmation

### Risks & Mitigation
| **Risk** | **Mitigation** |
|----------|----------------|
| Accidental cancellation | Require confirmation dialog with clear warning |
| Cancellation within 24 hours | Enforce 24-hour policy, show message if too late |
| Cancelled slot not released | Test thoroughly, use database transaction |

### Acceptance Criteria (Epic-Level)
- [ ] "My Appointments" page accessible from navigation
- [ ] Upcoming appointments listed in chronological order
- [ ] Past appointments listed in reverse chronological order
- [ ] Each appointment shows: doctor name, specialty, date, time, status
- [ ] "Cancel" button visible only for upcoming appointments
- [ ] Cancel disabled for appointments within 24 hours
- [ ] Confirmation dialog asks "Are you sure you want to cancel?"
- [ ] After cancellation: status updated to "Cancelled"
- [ ] Cancelled slot immediately available for booking by others
- [ ] Cancellation confirmation email sent
- [ ] Clear distinction between upcoming and past appointments (tabs or sections)

### Technical Considerations
- Query appointments by patient_id and status
- Calculate appointment date/time vs. current time for 24-hour rule
- Use soft delete pattern (status update, not record deletion)
- Audit log for cancellations (timestamp, user_id)
- Update slot availability in real-time (database trigger or application logic)

---

## EP-005: Provider Administration

### Epic Statement
**As an** administrator or practice manager
**I want to** manage doctor profiles and availability schedules
**So that** patients can find accurate provider information and book available time slots.

### Business Objective
- Enable practice control over provider listings
- Maintain accurate doctor information and availability
- Support practice operations with administrative tools
- Enable quick response to schedule changes
- Build foundation for multi-provider practice management

### Success Metrics
- 100% doctor profile accuracy
- <15 minutes average time to configure new doctor availability
- Zero booking discrepancies due to incorrect availability
- 95% admin user satisfaction with management tools

### User Personas
**Primary:**
- Practice administrators managing doctor listings
- Practice managers configuring schedules
- Individual doctors managing their own profiles (future)

**Secondary:**
- IT staff providing technical support

### Scope & Boundaries
**In Scope:**
- Create, read, update, delete doctor profiles
- Configure doctor details: name, specialty, bio, photo URL, contact info
- Set doctor status (Active/Inactive)
- Define working hours by day of week (e.g., Mon-Fri 9 AM - 5 PM)
- Set appointment slot duration (standardized at 30 minutes for MVP)
- Block specific time slots (e.g., lunch break, personal time)
- View all appointments for specific doctor
- Cancel appointments on behalf of doctor (with reason)
- Simple admin dashboard showing booking stats

**Out of Scope (Deferred):**
- Doctor self-service portal
- Bulk import doctors from CSV
- Advanced schedule templates (rotating schedules)
- PTO/vacation management workflow
- Multi-location doctor assignments
- Doctor billing/compensation tracking
- Real-time notifications to admin
- Advanced analytics and reporting
- Role-based admin permissions (single admin role for MVP)

### Dependencies
- Admin user authentication
- Database schema for doctors, availability, blocked slots
- Basic admin UI/dashboard

### Risks & Mitigation
| **Risk** | **Mitigation** |
|----------|----------------|
| Incorrect availability causes booking conflicts | Validation rules, preview before saving, testing |
| Accidental doctor deletion with existing appointments | Soft delete (status=inactive) instead of hard delete |
| Complex schedule patterns | Keep MVP simple, defer advanced patterns to Phase 2 |

### Acceptance Criteria (Epic-Level)
- [ ] Admin can access admin dashboard at `/admin`
- [ ] Admin can view list of all doctors
- [ ] Admin can create new doctor with form: name, specialty, bio, email, phone
- [ ] Admin can edit existing doctor information
- [ ] Admin can set doctor status to Active or Inactive
- [ ] Inactive doctors do not appear in patient search
- [ ] Admin can define working hours: select days, start time, end time
- [ ] System generates 30-minute slots based on working hours
- [ ] Admin can block specific date/time slots with reason
- [ ] Blocked slots not available for patient booking
- [ ] Admin can view all appointments for selected doctor (filterable by date)
- [ ] Admin can cancel any appointment with reason field
- [ ] Dashboard shows: total doctors, appointments today, appointments this week

### Technical Considerations
- Separate admin routes/controllers with authentication check
- Admin role flag in user table or separate admin table
- Slot generation algorithm: calculate slots between start/end time with 30-min intervals
- Exclude blocked slots from available slots query
- Soft delete pattern for doctors (status field)
- Form validation for working hours (start < end time, no overlaps)

---

## Epic Dependencies & Sequencing

### Development Priority
The epics should be developed in this sequence:

**Phase 1 - Foundation (Weeks 1-3):**
1. EP-001: User Authentication & Account Management
2. EP-005: Provider Administration (doctor profiles and availability setup)

**Phase 2 - Core Functionality (Weeks 3-6):**
3. EP-002: Doctor Discovery & Search
4. EP-003: Appointment Booking System

**Phase 3 - User Experience (Weeks 6-8):**
5. EP-004: Appointment Management

### Dependency Map
```
EP-001 (Auth) ──┬─→ EP-002 (Search) ──→ EP-003 (Booking) ──→ EP-004 (Management)
                │
                └─→ EP-005 (Admin) ──────────────┘
```

**Key Dependencies:**
- EP-002, EP-003, EP-004 all depend on EP-001 (users must be authenticated)
- EP-002 depends on EP-005 (doctors must exist to be searched)
- EP-003 depends on EP-002 (users find doctors, then book)
- EP-004 depends on EP-003 (appointments must exist to be managed)
- EP-005 can be developed in parallel with EP-001

---

## Traceability to Business Requirements

### Mapping Epics to BRD Objectives

| **BRD Business Objective** | **Supporting Epic(s)** |
|----------------------------|------------------------|
| Digitize appointment booking to reduce phone calls by 40% | EP-003, EP-004 |
| Increase booking conversion by 25% through 24/7 availability | EP-002, EP-003 |
| Improve practice efficiency by automating scheduling | EP-003, EP-005 |
| Validate product-market fit within 3 months | All Epics (MVP scope) |

### Mapping Epics to Success Criteria

| **BRD Success Criteria** | **Supporting Epic(s)** |
|--------------------------|------------------------|
| 500 registered patients within 3 months | EP-001 |
| 1,000 appointments booked in first quarter | EP-003 |
| 70% of new appointments booked online | EP-003, EP-002 |
| 80% of users complete booking in under 3 minutes | EP-003 |
| 75% user satisfaction score | EP-002, EP-003, EP-004 |
| <5% booking abandonment rate | EP-003 |
| 99% system uptime | All Epics (infrastructure) |
| Zero double-booking incidents | EP-003 |

---

## Out of Scope for MVP
The following potential epics are explicitly **deferred to future releases**:

- **Payment & Billing Epic:** Collecting payments, co-pays, and billing integration
- **Notifications & Reminders Epic:** Email/SMS appointment reminders, follow-up campaigns
- **Reviews & Ratings Epic:** Patient feedback, doctor ratings, testimonials
- **Telemedicine Epic:** Video consultations, virtual appointments
- **Patient Records Epic:** Medical history, EHR integration, document uploads
- **Advanced Analytics Epic:** Reporting dashboards, business intelligence
- **Mobile App Epic:** Native iOS/Android applications
- **Multi-Location Epic:** Support for practices with multiple clinics
- **Insurance Verification Epic:** Insurance eligibility checks, pre-authorization

---

## Epic Estimation Summary

| **Epic ID** | **Epic Name** | **Story Points** | **Estimated Weeks** |
|-------------|---------------|------------------|---------------------|
| EP-001 | User Authentication & Account Management | 13 | 1.5 weeks |
| EP-002 | Doctor Discovery & Search | 13 | 1.5 weeks |
| EP-003 | Appointment Booking System | 21 | 3 weeks |
| EP-004 | Appointment Management | 8 | 1 week |
| EP-005 | Provider Administration | 13 | 1.5 weeks |
| **TOTAL** | **All MVP Epics** | **68** | **8.5 weeks** |

**Note:** Story points use Fibonacci scale (1, 2, 3, 5, 8, 13, 21). Estimates include development and testing, exclude design and project management.

---

## Next Steps

1. **Review & Approval:** Stakeholders review this Epics document for completeness
2. **Feature Breakdown:** Decompose each epic into detailed features (see Features.md)
3. **User Story Writing:** Break features into user stories with acceptance criteria
4. **Sprint Planning:** Assign user stories to development sprints
5. **Design:** Create wireframes and UI mockups for each epic
6. **Development:** Build epics in priority sequence

---

## Document Change Log

| **Version** | **Date** | **Changes** | **Author** |
|-------------|----------|-------------|-----------|
| 1.0 | 2026-03-24 | Initial draft with 5 core epics | AI Planning Agent |

---

## Approval

| **Name** | **Role** | **Approval** | **Date** |
|----------|----------|--------------|----------|
| [Product Owner] | Product Owner | ☐ Approved | __________ |
| [Tech Lead] | Technical Lead | ☐ Approved | __________ |
| [UX Lead] | UX Designer | ☐ Approved | __________ |

**Next Document:** [Features.md](./Features.md) - Detailed feature breakdown for each epic
