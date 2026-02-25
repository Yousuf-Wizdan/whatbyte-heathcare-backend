# Healthcare Backend API

A secure backend system built with Django and Django REST Framework for managing patients, doctors, and their assignments.

## Run Locally

**Requirements**: Python 3.10 or higher (Python 3.11 recommended)

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
Create `.env` file by copying from the example:
```bash
cp .env.example .env
```

Then edit `.env` with your actual values:
```env
# Generate SECRET_KEY using:
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your_random_secret_key_here
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Environment Variables**:
- `SECRET_KEY`: Django secret key (required) - Generate using command above
- `DATABASE_URL`: PostgreSQL connection string (required) - Must include `?sslmode=require` for Neon
- `DEBUG`: Set to `True` for development, `False` for production
- `ALLOWED_HOSTS`: Comma-separated hostnames (for production, add your domain)

**Note**: Never commit your `.env` file to version control

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

All APIs have been manually tested using Postman. Follow this comprehensive test guide to verify all functionality.

### 🌐 Base URL
```
http://127.0.0.1:8000
```

---

## 🔐 AUTHENTICATION APIs

### 1. Register User
**POST** `/api/auth/register/`

**Body:**
```json
{
  "name": "Ritika Verma",
  "email": "ritika.verma92@gmail.com",
  "password": "StrongPass123"
}
```

**Expected:** User created successfully

---

### 2. Login
**POST** `/api/auth/login/`

**Body:**
```json
{
  "email": "ritika.verma92@gmail.com",
  "password": "StrongPass123"
}
```

**Response:** Copy the `access` token

**Important:** Use this token in all subsequent requests:
```
Authorization: Bearer <access_token>
```

---

## 👨‍⚕️ PATIENT MANAGEMENT APIs

### 3. Add Patient
**POST** `/api/patients/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "name": "Ananya Verma",
  "age": 28,
  "gender": "Female"
}
```

---

### 4. Get All Patients (User Specific)
**GET** `/api/patients/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Expected:** Shows only Ananya Verma (your own patients)

---

### 5. Get Specific Patient
**GET** `/api/patients/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 6. Update Patient
**PUT** `/api/patients/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "name": "Ananya Verma",
  "age": 29,
  "gender": "Female"
}
```

---

### 7. Delete Patient
**DELETE** `/api/patients/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 🩺 DOCTOR MANAGEMENT APIs

### 8. Add Doctor
**POST** `/api/doctors/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "name": "Dr. Vikram Khanna",
  "specialization": "Dermatology",
  "experience": 9
}
```

---

### 9. Get All Doctors
**GET** `/api/doctors/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 10. Get Specific Doctor
**GET** `/api/doctors/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 11. Update Doctor
**PUT** `/api/doctors/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "name": "Dr. Vikram Khanna",
  "specialization": "Dermatology",
  "experience": 10
}
```

---

### 12. Delete Doctor
**DELETE** `/api/doctors/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 🔗 PATIENT-DOCTOR MAPPING APIs

**Note:** Recreate patient & doctor first if deleted

### 13. Assign Doctor to Patient
**POST** `/api/mappings/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "patient": 1,
  "doctor": 1
}
```

---

### 14. Get All Mappings
**GET** `/api/mappings/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 15. Get Doctors for Specific Patient
**GET** `/api/mappings/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 16. Remove Doctor from Patient
**DELETE** `/api/mappings/1/`

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 🔐 SECURITY CHECK

### Test Without Token
**GET** `/api/patients/`

**Headers:** (Don't include Authorization header)

**Expected:** `401 Unauthorized`

---

## 🧪 VALIDATION CHECK

### Test Invalid Data
**POST** `/api/patients/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "name": "Test",
  "age": -5,
  "gender": "Male"
}
```

**Expected:** Validation error (age must be positive)

---

## ✅ EXPECTED OUTCOME

- ✔ Register works
- ✔ Login returns JWT access & refresh tokens
- ✔ Patients are user-owned (each user sees only their patients)
- ✔ Doctors are global (shared across all users)
- ✔ Mapping works with proper validation
- ✔ Unauthorized requests blocked (401)
- ✔ Validation works (negative age, invalid data rejected)

**If all pass → Assignment Complete 🎯**

---

## Project Overview

This is a **secure backend API** for healthcare management that provides:

- **Patient Management**: Users manage their own patients (full ownership control)
- **Doctor Directory**: Global directory accessible to all authenticated users
- **Doctor-Patient Assignments**: Secure assignment system with ownership validation

**Key Features**: JWT authentication, user-specific patient ownership, duplicate prevention, comprehensive validation.

## Tech Stack

- **Django** 5.1.5 & **Django REST Framework** 3.15.2
- **PostgreSQL** (Neon cloud database)
- **djangorestframework-simplejwt** 5.4.0 - JWT authentication
- **Python** 3.10+ (3.11 recommended)

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

## Production Deployment

### Prerequisites
1. PostgreSQL database (e.g., Neon, AWS RDS, Heroku Postgres)
2. Platform account (Heroku, Render, Railway, etc.)
3. Production WSGI server (gunicorn, uwsgi, etc.)

**Developer**: Yousuf Wizdan  
**Repository**: [github.com/Yousuf-Wizdan/whatbyte-heathcare-backend](https://github.com/Yousuf-Wizdan/whatbyte-heathcare-backend)
