# SIBO Diet API

SIBO Diet API is a backend service built with Flask, PostgreSQL, and Prisma (Python Client). It manages recipes, ingredients, pantry tracking, meal planning, and automated shopping list generation based on weekly schedules and dietary goals. The architecture is modular and prepared for future scaling or migration.

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Framework:** Flask
* **Database:** PostgreSQL 17
* **ORM:** Prisma ORM (Python client)
* **Authentication:** Supabase (JWT authentication)
* **CLI tool:** Node.js (Prisma CLI only)

## 📂 Project Structure

```text
sibo-diet-api/
├── src/
│   ├── db/
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   └── app.py
├── prisma/
├── venv/
├── .env
├── requirements.txt
└── README.md
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USER/sibo-diet-api.git
cd sibo-diet-api
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install flask prisma python-dotenv
```

### 4. Install Node.js & PostgreSQL
Prisma CLI requires Node.js. If missing, install it along with PostgreSQL via Homebrew:

```bash
# Install Node.js
brew install node

# Install and start PostgreSQL 17
brew install postgresql@17
brew services start postgresql@17

# Create the database
createdb sibo_diet
```

### 5. Environment Variables
Create a `.env` file in the root directory:

```env
DATABASE_URL="postgresql://USER@localhost:5432/sibo_diet"
```

### 6. Prisma Setup
Generate the Prisma client and apply schema changes:

```bash
# Generate client
python -m prisma generate

# Apply changes directly (Development)
python -m prisma db push

# Alternative: Apply via migrations
python -m prisma migrate dev --name init
```

### 7. Run the Project
```bash
python src/app.py
```

## 📊 Database Overview

### Entities
* `Users`
* `Recipes`
* `Ingredients`
* `RecipeIngredients`
* `PantryItems`
* `CalendarWeeks`
* `CalendarDays`
* `MealEntries`
* `ShoppingLists`
* `ShoppingItems`
* `TrackingWeeks`
* `IngredientHistory`

### Core Logic
* **Pantry:** Stores user-owned ingredients and persists them across weeks.
* **Shopping Lists:** Generated dynamically based on weekly meal plans and recipes.
* **Calendar System:** Manages weekly structures and daily meal scheduling.

## 🔐 Authentication

* Powered by Supabase JWT authentication.
* No password storage in the backend database.
* Users are automatically synced into Prisma after external authentication.

## 🔄 Prisma Workflow

### Installation & Initialization
```bash
pip install prisma
python -m prisma generate
```

### Development Commands
* **Apply schema changes directly:** `python -m prisma db push`
* **Create a new migration:** `python -m prisma migrate dev --name init`
* **Update an existing model:** `python -m prisma migrate dev --name update_model`
* **Deploy migrations (Production):** `python -m prisma migrate deploy`
* **Reset database (Destructive):** `python -m prisma migrate reset`
* **Run port tunnel:**
```bash
cd ~/sibo-diet-api
source venv/bin/activate
python main.py
```

### Typical Workflows

#### Scenario A: Adding a new table
1. Edit `schema.prisma`
2. Run `python -m prisma db push` (or `python -m prisma migrate dev --name add_new_table`)
3. Regenerate client: `python -m prisma generate`

#### Scenario B: Modifying an existing model
1. Edit `schema.prisma`
2. Run `python -m prisma migrate dev --name update_model` (or `python -m prisma db push` for a quick sync)

## 📌 Important Notes

* Prisma Python runs **async** internally.
* **Always** regenerate the Prisma client after schema changes.
* Prefer **migrations** (`prisma migrate`) for production environments.
* Use **db push** (`prisma db push`) only for fast, local prototyping.
