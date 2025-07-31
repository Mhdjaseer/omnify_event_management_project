
# 🎉 Event Management System API

A simple and scalable REST API built using Django and Django REST Framework (DRF) for managing events and attendee registrations. This system supports time zone-aware event listings, attendee registration, and pagination.

---

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
- **Database**: PostgreSQL / SQLite
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

## ⚙️ Environment Variables (`.env`)

Create a `.env` file for your secret settings:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL
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
├── event_manager/
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── requirements.txt
```

---

## 📌 Future Enhancements

- ✅ Email notifications for attendees
- ✅ Event categories/tags
- ✅ Admin dashboard (optional)
- ✅ Rate limiting and throttling
- ✅ Async support (with Django 4+)

---

## 🧑‍💻 Author

Made with ❤️ by [Your Name](https://github.com/your-username)

---

## 📄 License

This project is licensed under the MIT License.
