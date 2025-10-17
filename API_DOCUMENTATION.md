# Job Haunt API - Complete Documentation

## Overview

A comprehensive Django REST Framework API for job application tracking, learning management, and user management with JWT authentication including role-based access control.

## Features

- ✅ **JWT Authentication** with custom claims (role included in token)
- ✅ **Token Refresh** with automatic role propagation
- ✅ **Token Blacklist** for secure logout
- ✅ **Forgot Password** functionality with email-based reset
- ✅ **Role-Based Access Control** (User/Admin)
- ✅ **Swagger/OpenAPI Documentation** (drf-spectacular)
- ✅ **ListAPIView** and **RetrieveUpdateDestroyAPIView** for all models
- ✅ **User Management** (Users, Profiles, Skills)
- ✅ **Job Application Tracking**
- ✅ **Learning Management System**

## Tech Stack

- **Django 5.2.7**
- **Django REST Framework 3.16.1**
- **Simple JWT 5.5.1** (with crypto support)
- **drf-spectacular 0.28.0** (Swagger/OpenAPI)
- **SQLite** (Development database)

## Installation & Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login (get JWT tokens with role) | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| POST | `/api/auth/logout/` | Logout (blacklist token) | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |
| POST | `/api/auth/forgot-password/` | Request password reset | No |
| POST | `/api/auth/reset-password/` | Reset password with token | No |
| GET | `/api/auth/me/` | Get current user info | Yes |

### User Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users (Admin only) | Yes (Admin) |
| POST | `/api/users/` | Create user (Admin only) | Yes (Admin) |
| GET | `/api/users/{id}/` | Get user details | Yes |
| PUT/PATCH | `/api/users/{id}/` | Update user | Yes |
| DELETE | `/api/users/{id}/` | Delete user (Admin only) | Yes (Admin) |

### Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profiles/` | List profiles | Yes |
| GET | `/api/profiles/{id}/` | Get profile details | Yes |
| PUT/PATCH | `/api/profiles/{id}/` | Update profile | Yes |
| DELETE | `/api/profiles/{id}/` | Delete profile | Yes |

### User Skills Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/user-skills/` | List user skills | Yes |
| POST | `/api/user-skills/` | Add skill to profile | Yes |
| GET | `/api/user-skills/{id}/` | Get skill details | Yes |
| PUT/PATCH | `/api/user-skills/{id}/` | Update skill | Yes |
| DELETE | `/api/user-skills/{id}/` | Remove skill | Yes |

### Job Application Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/job-applications/` | List job applications | Yes |
| POST | `/api/job-applications/` | Create job application | Yes |
| GET | `/api/job-applications/{id}/` | Get application details | Yes |
| PUT/PATCH | `/api/job-applications/{id}/` | Update application | Yes |
| DELETE | `/api/job-applications/{id}/` | Delete application | Yes |

### Job Skills & Status Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/job-skills/` | List job skills | Yes |
| POST | `/api/job-skills/` | Create job skill | Yes |
| GET/PUT/PATCH/DELETE | `/api/job-skills/{id}/` | Manage job skill | Yes |
| GET | `/api/job-statuses/` | List application statuses | Yes |
| POST | `/api/job-statuses/` | Create status | Yes |
| GET/PUT/PATCH/DELETE | `/api/job-statuses/{id}/` | Manage status | Yes |

### Learning Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/learning-plans/` | List learning plans | Yes |
| POST | `/api/learning-plans/` | Create learning plan | Yes |
| GET/PUT/PATCH/DELETE | `/api/learning-plans/{id}/` | Manage learning plan | Yes |
| GET | `/api/learning-resources/` | List learning resources | Yes |
| POST | `/api/learning-resources/` | Create resource | Yes |
| GET/PUT/PATCH/DELETE | `/api/learning-resources/{id}/` | Manage resource | Yes |
| GET | `/api/learning-statuses/` | List learning statuses | Yes |
| POST | `/api/learning-statuses/` | Create status | Yes |
| GET/PUT/PATCH/DELETE | `/api/learning-statuses/{id}/` | Manage status | Yes |

## JWT Authentication

### Custom Token Claims

The JWT tokens include the following custom claims:

```json
{
  "token_type": "access",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique-token-id",
  "user_id": 1,
  "role": "user",
  "email": "user@example.com",
  "username": "johndoe"
}
```

### Using JWT Tokens

1. **Register or Login** to get tokens:

```bash
POST /api/auth/login/
{
  "username": "johndoe",
  "password": "password123"
}
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

2. **Use Access Token** in requests:

```bash
Authorization: Bearer <access_token>
```

3. **Refresh Token** when access token expires:

```bash
POST /api/auth/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

4. **Logout** to blacklist token:

```bash
POST /api/auth/logout/
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Password Reset Flow

### 1. Request Password Reset

```bash
POST /api/auth/forgot-password/
{
  "email": "user@example.com"
}
```

Response:
```json
{
  "message": "If the email exists, a password reset link has been sent"
}
```

### 2. Check Email

User receives an email with:
- Reset link
- Reset token

### 3. Reset Password

```bash
POST /api/auth/reset-password/
{
  "token": "reset-token-from-email",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

## Example Usage

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

### Create a Job Application

```bash
curl -X POST http://localhost:8000/api/job-applications/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "position": "Senior Developer",
    "company_name": "Tech Corp",
    "location": "San Francisco, CA",
    "applied_date": "2024-01-15",
    "status": 1,
    "skills": [1, 2, 3],
    "description": "Full-stack development role",
    "required_experience": 5,
    "application_through": "website",
    "user": 1
  }'
```

### Get Current User Profile

```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

## Models Overview

### User Management
- **CustomUser**: Extended user model with role field
- **Profile**: User profile with bio and images
- **UserSkills**: User's skills with proficiency levels

### Job Management
- **JobApplication**: Job application tracking
- **JobApplicationStatus**: Application status (open, applied, interview, etc.)
- **JobSkills**: Available job skills

### Learning Management
- **LearningManagement**: Learning plans/courses
- **LearningResource**: Learning resources (videos, articles, books)
- **LearningManagementStatus**: Learning progress status

### Authentication
- **PasswordResetToken**: Secure password reset tokens

## Security Features

- ✅ JWT tokens with 60-minute expiry
- ✅ Refresh tokens with 7-day expiry
- ✅ Token rotation on refresh
- ✅ Token blacklisting on logout
- ✅ Role-based access control
- ✅ Password reset with 24-hour token expiry
- ✅ Email enumeration protection
- ✅ CORS configuration ready
- ✅ Permission-based endpoint access

## Testing with Swagger

1. Navigate to http://localhost:8000/api/docs/
2. Click "Authorize" button
3. Enter: `Bearer <your_access_token>`
4. Test any endpoint directly from the UI

## Environment Variables (Production)

For production, set these environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-database-url

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

## Next Steps

1. ✅ Run migrations: `python manage.py migrate`
2. ✅ Create superuser: `python manage.py createsuperuser`
3. ✅ Configure email settings for password reset
4. ✅ Test endpoints via Swagger UI
5. ✅ Customize permissions as needed
6. ✅ Add CORS headers for frontend integration
7. ✅ Deploy to production

## Support

For issues or questions, refer to:
- Django REST Framework: https://www.django-rest-framework.org/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/
- drf-spectacular: https://drf-spectacular.readthedocs.io/
