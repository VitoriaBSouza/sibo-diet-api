# sibo-diet-api
SIBO Diet API is a backend service built with Flask, PostgreSQL, and Prisma. It manages recipes, ingredients, meal planning, pantry tracking, and automated shopping list calculations based on weekly schedules and user dietary goals. The system is designed with a modular architecture to support future migration to FastAPI and Go.

# SIBO Diet API

Backend for a nutrition and meal planning system focused on tracking recipes, ingredients, pantry inventory, weekly planning, and dynamic shopping list generation.

---

# Tech Stack

- Python 3.9+
- Flask
- PostgreSQL 17
- Prisma ORM (Python client)
- JWT Authentication (Supabase)
- Node.js (Prisma CLI only)

---

# Project Structure

sibo-diet-api/
├── backend/

├── prisma/

├── .env

├── venv/

└── README.md

---

# Installation

## Clone repository
```bash
git clone https://github.com/YOUR_USER/sibo-diet-api.git
cd sibo-diet-api

Create Python environment
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install flask prisma
Install PostgreSQL
brew install postgresql@17
brew services start postgresql@17
createdb sibo_diet
Install Node.js (Prisma)
node -v
npm -v

If missing:

brew install node
Initialize Prisma
prisma init
Configure environment

Create .env:

DATABASE_URL="postgresql://USER@localhost:5432/sibo_diet"
Run migrations
prisma migrate dev --name init
Generate Prisma client
prisma generate
Run project
python app.py
Database Overview
Entities
Users
Recipes
Ingredients
RecipeIngredients
Pantry
CalendarWeeks
CalendarDays
MealEntries
ShoppingLists
Core Logic
Pantry

Stores user-owned ingredients and persists across weeks.

Shopping List

Generated dynamically from selected weeks and recipes. Does not store state.

Weekly Planning

Defines meal schedule and drives shopping calculations.

Authentication
Supabase JWT authentication
No passwords stored in backend