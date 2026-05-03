# Running Kashmiri Heritage Locally

This guide provides the steps to start the database, backend, and frontend for local development.

## Prerequisites
- **Python 3.x** installed.
- **Node.js & npm** installed.
- **MySQL 8.0** (located in your Downloads folder as per your environment).

---

## Step 1: Start the MySQL Database
Open a new terminal and run:
```powershell
# Navigate to the bin directory of your MySQL installation and start the server
cd "C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits"
..\..\Downloads\mysql-8.0.45-winx64\mysql-8.0.45-winx64\bin\mysqld --console
```

## Step 2: Start the Backend (Flask)
Open a second terminal and run:
```powershell
# 1. Navigate to the project root
cd "C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits"

# 2. Activate the virtual environment
.\backend\venv\Scripts\activate

# 3. (Optional) Set Flask to Development mode for better debugging
$env:FLASK_CONFIG="dev"

# 4. Start the server
py .\backend\app.py
```
> [!TIP]
> The backend will be available at `http://localhost:5000`.

## Step 3: Start the Frontend (Vue.js + Vite)
Open a third terminal and run:
```powershell
# 1. Navigate to the frontend directory
cd "C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits\frontend"

# 2. Start the development server
npm run dev -- --port 3000
```
> [!TIP]
> The frontend will be available at `http://localhost:3000`.

---

## Troubleshooting & Tips

### API Connection
Ensure your `.env` file in the `frontend` folder (or environment variables) points to the local backend:
```env
VITE_API_URL=http://localhost:5000
```

### Database Connection
If you encounter database errors, ensure the `DATABASE_URL` in `backend/.env` is set correctly for your local MySQL instance:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost/kashmiri_dry_fruits
```

### One-Click Start (Automation)
You can create a `start_all.ps1` script in the root directory to open all three terminals at once:

```powershell
# Start Database
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits'; ..\..\Downloads\mysql-8.0.45-winx64\mysql-8.0.45-winx64\bin\mysqld --console"

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits'; .\backend\venv\Scripts\activate; `$env:FLASK_CONFIG='dev'; py .\backend\app.py"

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits\frontend'; npm run dev"
```
