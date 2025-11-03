🧭 Chaperone Backend
====================

The **Chaperone Backend** is a **Django-based REST API service** that powers the _Chaperone Platform_ — a system that connects **wanderers** (users seeking company) with **walkers** (companions/guides) for shared walking experiences.

It’s built with a modular architecture, featuring account management, walk scheduling, feedback, payments, and live location tracking — all optimized for real-time performance using **Daphne (ASGI)**.

* * *

🚀 Features
-----------

*   **Authentication & User Roles**
    *   Email/phone login with OTP
    *   Role distinction: _Wanderer_ & _Walker_
*   **Walk Management**
    *   Real-time room creation for live walks
    *   Scheduling & walk session tracking
*   **Feedback System**
    *   Mutual feedback between Wanderers & Walkers
*   **Payments**
    *   Fee handling & linked payment records
*   **Preferences**
    *   Gender, mobility, charity, languages & pace preferences
*   **Live Location Sharing**
    *   Real-time latitude/longitude updates using Rooms

* * *

🧩 Project Structure
--------------------

```
Chaperone-backend/
├── accounts/                 # User management
├── accounts_auth/            # Authentication / OTP logic
├── chaperone/                # Core Django project configuration
├── feedback/                 # Feedback & rating logic
├── payments/                 # Payment and billing
├── search/                   # Search and discovery features
├── walkRequests/             # Walk request and approval logic
├── walks/                    # Active and completed walks
├── db.sqlite3                # Development database
├── manage.py                 # Django management utility
├── requirements.txt          # Dependencies
└── doc.md                    # API documentation
```

* * *

🗄️ Database Schema Overview
----------------------------

The backend uses a **normalized relational schema** for user management, walk sessions, and feedback.

### Core Tables:

*   **`user`** → base user info, roles, OTP, verification
*   **`wanderer` / `walker`** → profile extensions
*   **`requests`** → walk booking requests
*   **`walks`** → ongoing/completed walks
*   **`room`** → active room between walker & wanderer
*   **`live_location`** → tracks location in real time
*   **`feedback`** → ratings and comments
*   **`payment`** → records transaction info


Explore the complete Chaperone Database Schema with entity relationships and table references here:

<img width="3893" height="2494" alt="Chaperone" src="https://github.com/user-attachments/assets/7831ae37-c2d0-462b-ab4f-dbebdf8b52a9" />
[View Schema on dbdiagram.io](https://dbdiagram.io/d/Chaperone-68f08a902e68d21b41b93b48)

* * *

🛠️ Tech Stack
--------------

| Component | Technology |
| --- | --- |
| **Backend Framework** | Django (Python) |
| **Server** | **Daphne (ASGI)** |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Authentication** | Django Auth + OTP |
| **API Format** | REST |
| **Deployment** | Daphne + systemd / nohup compatible |

* * *

⚙️ Setup Instructions
---------------------

### 1\. Clone the Repository

```bash
git clone https://github.com/Agrawal-Sujal/Chaperone-backend.git
cd Chaperone-backend
```

### 2\. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Apply Migrations

```bash
python manage.py migrate
```

### 5\. Run Server with Daphne

```bash
daphne -b 0.0.0.0 -p 8000 chaperone.asgi:application
```

### 6\. Access the API

Visit:

```
http://127.0.0.1:8000/
```

Or replace `127.0.0.1` with your server IP for remote access.

* * *

🧑‍💻 Development Tips
----------------------

*   Use **SQLite** for quick local development
*   Switch to **PostgreSQL** in production (`DATABASES` setting in `settings.py`)
*   Use **Daphne** for async support (e.g., WebSockets, live location updates)
*   For persistent background running (Linux):
    ```bash
    nohup daphne -b 0.0.0.0 -p 8000 chaperone.asgi:application > daphne.log 2>&1 &
    ```
*   To view logs:
    ```bash
    tail -f daphne.log
    ```

* * *

