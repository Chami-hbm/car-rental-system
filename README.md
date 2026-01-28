# 🚗 MC Car Rental System
*Advanced OOP-based Car Rental Management System*

## 🔥 Key Features
- **Role-Based Access**: Admin & Customer portals
- **Loyalty Rewards**: 5% discount for timely repeat customers
- **Smart Overlap Detection**: Prevents double-booking conflicts
- **Secure Authentication**: bcrypt password hashing
- **Dynamic Pricing**: Real-time discount calculations

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue?logo=mysql)
![OOP](https://img.shields.io/badge/OOP-Design-blue)
![Design Patterns](https://img.shields.io/badge/Singleton-Factory-orange)

## 📁 Project Structure
```
car-rental-system/
├── src/                   # Source code
├── database/              # SQL scripts
├── docs/                  # Documentation
├── tests/                 # Unit tests
├── .env.example           # Configuration template
├── requirements.txt
└── README.md
```
## 💡 Innovative Feature: Loyalty Discount
5% discount for customers who return within 30 days
```
def calculate_discount(user):
    if user.rentals_count >= 1 and user.last_rental_date:
        days_since_last = (datetime.today() - user.last_rental_date).days
        if days_since_last <= 30:
            return 0.95  # 5% discount
    return 1.0
```
## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MySQL Server

## Installation
```bash
# 1. Clone repository
git clone https://github.com/chami-hbm/car-rental-system

# 2. Setup database
mysql -u root -p < database/schema.sql

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python src/main.py
```
