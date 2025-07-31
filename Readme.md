
# 🎉 Event Management System API

> ⚙️ **Production-ready** Django REST API for event and attendee management.

A simple and scalable REST API built using Django and Django REST Framework (DRF) for managing events and attendee registrations. This system supports time zone-aware event listings, attendee registration, and pagination.

---

## ⚠️ Note for Production

- This project is designed to be **production-level**.
- When deploying via Docker in production, make sure to:
  - ✅ **Uncomment** the `gunicorn` command in the `Dockerfile`:
    ```dockerfile
    # CMD ["gunicorn", "event_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
    ```
  - ✅ **Uncomment** or include `gunicorn` in your `requirements.txt`:
    ```
    gunicorn>=21.2.0
    ```
"""

## 🧰 Features

- ✅ Create, List, Update, and Delete Events
- ✅ Register Attendees for Events
- ✅ List Attendees by Event
- ✅ Paginated Event Listings
- ✅ Timezone-aware Event Start Times
- ✅ Modular Service Layer
- ✅ Logging and Error Handling

---

## 🚀 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**:SQLite
- **Time Handling**: `pytz`, `django.utils.timezone`
- **Testing**: Django TestCase
- **Logging**: Python `logging` module

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/event-management-api.git
cd event-management-api
```

### 2. Create Virtual Environment and Activate

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Server

```bash
python manage.py runserver
```

---
### 🐳 Option 2: Run with Docker

#### 1. Build and Run

```bash
docker compose up --build 

```

## ⚙️ Environment Variables (`.env`)

Create a `.env` file for your secret settings:

```
#No needs default value already added in setting.py 
DEBUG=True
SECRET_KEY=your-secret-key
```

---

## 📦 API Endpoints

### 🔹 Events

| Method | Endpoint               | Description                      |
|--------|------------------------|----------------------------------|
| GET    | `/api/events/`         | List upcoming events             |
| POST   | `/api/events/`         | Create a new event               |
| GET    | `/api/events/<id>/`    | Retrieve event details           |
| PUT    | `/api/events/<id>/`    | Update an event                  |
| DELETE | `/api/events/<id>/`    | Delete an event                  |

🔸 Supports `timezone` query param for listing in user's timezone. Default: `Asia/Kolkata`.

---

### 🔹 Attendees

| Method | Endpoint                            | Description                  |
|--------|-------------------------------------|------------------------------|
| POST   | `/api/events/<event_id>/register/` | Register a new attendee      |
| GET    | `/api/events/<event_id>/attendees/`| List all attendees for event |

---

## 🧪 Running Tests

```bash
python manage.py test
OR 
docker exec -it django_event_app python manage.py test_seed
```

---

## 🪵 Logging

Basic logging is enabled and prints to the console.

You can customize it in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## 🗃 Project Structure

```
.
├── events/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── tests.py
├── omnify_eventora/
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── requirements.txt
```

---

---

## 🧪 Load Demo Data

You can populate the database with sample events and attendees using the provided scripts.

### 🔹 On Windows

Run the `.bat` file:

```bash
.\seed_demo.bat
```

### 🔹  On macOS/Linux

Run the `.sh` file:

```
chmod +x seed_demo.sh
./seed_demo.sh
```
### 🔹 OR
```
docker exec -it django_event_app python manage.py test_seed^C
```