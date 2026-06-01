# 🏢 RTDMS — Real Time Data Management System

## 📌 Overview

RTDMS is a **role-based organizational management system** designed to handle:

* User authentication & role control
* Department and unit hierarchy
* Task/report submission workflows
* Structured supervision and accountability

The system enforces a **clear chain of command**, ensuring proper data flow from staff to top-level administrators.

---

# 🧠 System Architecture

RTDMS follows a **modular Django architecture**:

```
accounts/     → Authentication & user management  
dashboards/   → User dashboards based on roles  
templates/    → UI templates  
static/       → CSS, JS, assets  
config/       → Project settings & routing  
```

---

# 🏗️ Organizational Hierarchy (Core Logic)

The entire system is built on a **strict hierarchical structure**:

```
ADMIN
   ↓
DEPARTMENT
   ↓
DEPARTMENT HEAD
   ↓
UNIT
   ↓
UNIT HEAD
   ↓
SUPERVISOR
   ↓
STAFF
```

---

# 🎯 Role Responsibilities

## 🔹 ADMIN

* Full system access
* Creates:

  * Departments
  * Units
  * Users
* Assigns roles

---

## 🔹 DEPARTMENT

* Top-level organizational division
* Example:

  * IT
  * HR
  * Finance

Each department:

* Has **one Department Head**
* Contains multiple units

---

## 🔹 DEPARTMENT HEAD

* Oversees entire department
* Manages all units under the department
* Reports to Admin

---

## 🔹 UNIT

* Subdivision of a department

Example:

```
IT Department
   ├── Backend Unit
   ├── Network Unit
   └── Support Unit
```

---

## 🔹 UNIT HEAD

* Leads a specific unit
* Reports to Department Head

---

## 🔹 SUPERVISOR

* Handles daily operations
* Oversees staff within a unit

---

## 🔹 STAFF

* Regular users
* Submit reports and tasks


---

# ⚙️ Validation Rules (Critical)

| Role       | Department     | Unit           |
| ---------- | -------------- | -------------- |
| ADMIN      | ❌ Not required | ❌ Not required |
| DEPT_HEAD  | ✅ Required     | ❌ Not required |
| UNIT_HEAD  | ✅ Required     | ✅ Required     |
| SUPERVISOR | ✅ Required     | ✅ Required     |
| STAFF      | ✅ Required     | ✅ Required     |

---

# 🔄 System Flow (Visual Representation)

## 🧭 Command Flow

```
[ADMIN]
   │
   ├── Creates Departments
   │
   └── Assigns Department Heads
            │
            ▼
    [DEPARTMENT HEAD]
            │
            ├── Manages Units
            │
            ▼
        [UNIT HEAD]
            │
            ├── Assigns Supervisors
            │
            ▼
        [SUPERVISOR]
            │
            ├── Oversees Staff
            │
            ▼
          [STAFF]
```

---

## 📊 Data Flow (Reports / Tasks)

```
STAFF → SUPERVISOR → UNIT HEAD → DEPARTMENT HEAD → ADMIN
```

---

# 👤 User Profile Structure

Each user contains:

### Identity

* Email
* First Name
* Last Name

### Role & Access

* Role
* Department
* Unit

### Profile Data

* Profile Image
* Gender

---

# 🔐 Authentication Flow

```
User Login
   ↓
Role Detection
   ↓
Redirect to Role-Based Dashboard
```

---

# 🖥️ Dashboard Behavior

Each role sees a **different dashboard**:

| Role       | Dashboard Access       |
| ---------- | ---------------------- |
| Admin      | Full system            |
| Dept Head  | Department overview    |
| Unit Head  | Unit-specific data     |
| Supervisor | Team management        |
| Staff      | Personal tasks/reports |

---

# 📁 File Upload (Profile Images)

* Stored in:

```
/media/profiles/
```

* Config:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

Features:

* Auto logout on inactivity
* Session reset on activity
* Secure access control

---

# 🚀 Key Features

* ✅ Custom user model (email-based login)
* ✅ Role-based access control
* ✅ Department-unit hierarchy
* ✅ Profile image upload
* ✅ Secure authentication
* ✅ Scalable architecture

---

# ⚠️ Design Considerations

### 1. Single Department/Unit Limitation

* Each user belongs to:

  * One department
  * One unit

Future upgrade:
→ Many-to-many relationships

---

### 2. Role Dependency

System relies heavily on roles
→ Must enforce validation strictly

---

# 🧪 Running the Project

```bash
# Clone repo
git clone <repo-url>

# Create virtual environment
python -m venv myenv

# Activate
myenv\Scripts\activate

# Install dependencies
pip install -r requirement.txt

# Run server
python manage.py runserver
```

---

# 📌 Conclusion

RTDMS is built around a **clear hierarchical structure** ensuring:

* Accountability
* Organized data flow
* Role-based access control

The architecture is designed to be:

* **Scalable**
* **Maintainable**
* **Secure**

---

# ⚠️ Limitation / Counterpoint

This design assumes a **strict linear hierarchy**.
In real-world organizations:

* Users may belong to multiple units
* Cross-department collaboration may exist

→ Future iterations may require **many-to-many relationships and flexible role mapping**

---
