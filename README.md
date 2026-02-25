# Healthcare Backend API

A secure backend system built with Django and Django REST Framework for managing patients, doctors, and their assignments.

## Run Locally

### 1. Clone & Setup
```bash
git clone https://github.com/Yousuf-Wizdan/whatbyte-heathcare-backend.git
cd whatbyte-heathcare-backend
python -m venv venv
```

**Activate virtual environment:**
- Mac/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create `.env` file:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
DEBUG=True
```
**Note**: For Neon databases, include `?sslmode=require` in DATABASE_URL

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Test with Postman
1. **Register**: `POST /api/auth/register/` with name, email, password
2. **Login**: `POST /api/auth/login/` to get JWT tokens
3. **Use APIs**: Add `Authorization: Bearer <token>` header for protected endpoints

---

## Testing

All APIs have been manually tested using Postman.

### Test Flow

Follow this sequence:

1. **Register User**  
   `POST /api/auth/register/`

2. **Login**  
   `POST /api/auth/login/`  
   Use returned JWT access token.

3. **Create Patient**  
   `POST /api/patients/`

4. **Create Doctor**  
   `POST /api/doctors/`

5. **Assign Doctor to Patient**  
   `POST /api/mappings/`

6. **Retrieve Mappings**  
   `GET /api/mappings/`

7. **Remove Mapping**  
   `DELETE /api/mappings/<id>/`

### Security Tests Verified

- ✅ Unauthorized requests return 401
- ✅ Users cannot access other users' patients
- ✅ Duplicate doctor assignments are prevented
- ✅ Invalid data (e.g., negative age) is rejected

---

## Project Overview

This is a **secure backend API** for healthcare management that provides:

- **Patient Management**: Users manage their own patients (full ownership control)
- **Doctor Directory**: Global directory accessible to all authenticated users
- **Doctor-Patient Assignments**: Secure assignment system with ownership validation

**Key Features**: JWT authentication, user-specific patient ownership, duplicate prevention, comprehensive validation.

## Tech Stack

- **Django** 6.0.2 & **Django REST Framework** 3.14.0
- **PostgreSQL** (Neon cloud database)
- **djangorestframework-simplejwt** 5.3.1 - JWT authentication
- **Python 3.x**

## Features

- ✅ Secure user registration & login (email-based)
- ✅ JWT-protected APIs with token refresh
- ✅ Patient ownership control (users only access their own patients)
- ✅ Global doctor management (shared across users)
- ✅ Doctor assignment to patients with duplicate prevention
- ✅ Validation & error handling (age: 0-150, password min 8 chars)

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Patients (JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients/` | Create patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Get patient details |
| PUT/PATCH | `/api/patients/<id>/` | Update patient |
| DELETE | `/api/patients/<id>/` | Delete patient |

### Doctors (JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/` | Create doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get doctor details |
| PUT/PATCH | `/api/doctors/<id>/` | Update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |

### Mappings (JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mappings/` | Assign doctor to patient |
| GET | `/api/mappings/` | List your mappings |
| GET | `/api/mappings/<patient_id>/` | Get patient's doctors |
| DELETE | `/api/mappings/<id>/` | Remove assignment |

## Security

- 🔒 JWT Bearer token authentication
- 🔒 Patient ownership enforcement (users can only access their own patients)
- 🔒 Duplicate assignment prevention
- 🔒 Comprehensive validation (age range, password strength, email uniqueness)

## Expected Outcome

Users can:
- Register and login to receive JWT tokens
- Manage their own patients (CRUD operations)
- View and manage all doctors in the system
- Assign doctors to their patients with ownership validation
- Cannot access or modify other users' patients

## Future Improvements

- Role-based access control (Admin, Doctor, Patient roles)
- Appointment scheduling system
- Audit logs for compliance
- Email notifications
- Advanced search & filtering

---

**Developer**: Yousuf Wizdan  
**Repository**: [github.com/Yousuf-Wizdan/whatbyte-heathcare-backend](https://github.com/Yousuf-Wizdan/whatbyte-heathcare-backend)
