# 🎬 BookASeat
### Online Movie & Event Ticket Booking System (Django)

BookASeat is a full-stack web-based ticket booking platform built using Django.  
It allows users to browse movies and events, select seats, and complete bookings through a secure authentication system.

This project was developed as a college academic project to demonstrate backend architecture, database design, authentication handling, and collaborative Git workflow.

---

## 🚀 Features

### 👤 User Features
- User registration & login (Django Authentication)
- Browse movies and events
- View show timings
- Interactive seat selection
- Booking confirmation
- Booking history page

### 🎟 Booking System
- Many-to-Many relationship between Booking and Seats
- One-to-One relationship between Booking and Payment
- Prevention of double booking
- Transaction-safe booking logic

### 🛠 Admin Features
- Admin dashboard
- Add/Edit/Delete:
  - Movies
  - Theatres
  - Shows
  - Events
  - Venues
- Manage users and bookings

---

## 🏗 System Architecture

The project follows a layered architecture:

- Presentation Layer → Django Templates + Bootstrap 5  
- Application Layer → Django Views & Business Logic  
- Data Layer → SQLite Database (Django ORM)

---

## 🧰 Technology Stack

### Backend
- Python 3.x
- Django 5.x

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons

### Database
- SQLite (Development)

### Version Control
- Git & GitHub (Branch-based workflow)

---

## 📂 Project Structure

```
bookaseat/
│
├── movies/        # Movie & show management
├── bookings/      # Seat booking logic
├── payments/      # Payment simulation
├── events/        # Event management
├── dashboard/     # Admin dashboard
├── templates/     # Global templates
├── media/         # Uploaded posters/images
└── config/        # Project settings
```

---

## 🔐 Security Measures

- CSRF Protection enabled
- Authentication-based access control
- POST-based logout
- Admin restricted to staff users
- Atomic transactions to prevent race conditions

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone <your-repo-link>
cd bookaseat
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```
python manage.py migrate
```

### 5️⃣ Create Superuser

```
python manage.py createsuperuser
```

### 6️⃣ Run Server

```
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/
```

---

## 🧪 Testing Flow

1. Login or register
2. Browse movies
3. Select show
4. Choose seats
5. Confirm booking
6. View booking history

---

## 📊 Database Relationships

- Movie → Show (One-to-Many)
- Show → Seat (One-to-Many)
- Booking ↔ Seat (Many-to-Many)
- Booking → Payment (One-to-One)

---

## 🔄 Git Workflow

- `main` → Stable branch
- `ui-dev` → UI development branch
- Feature-based branch development
- Controlled merge into main after testing

---

## 📌 Future Enhancements

- Real payment gateway integration
- Email/SMS booking confirmation
- Real-time seat locking (WebSockets)
- Cloud deployment (AWS/Azure)
- Advanced analytics dashboard

---

## 👨‍💻 Team Members

- Project Lead – (Your Name)
- Backend Developer – (Name)
- Frontend Developer – (Name)
- QA / Testing – (Name)

---

## 📄 License

This project is developed for academic purposes.
