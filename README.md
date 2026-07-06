# EZEmployee

EZEmployee is an AI-powered HR dashboard built with Streamlit. It provides employee management, analytics, and reporting features using a CSV-backed dataset.

## Features

- Dashboard overview with charts and performance metrics
- Employee CRUD: add, update, delete, search, import, export
- AI analytics: performance prediction, attrition risk scoring, and clustering
- PDF report generation utilities

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Arshpreet0005/EZEmployee.git
cd EZEmployee/EZEmployee
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

PowerShell:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Command Prompt:
```cmd
.\.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

### 6. Open in browser

After startup, open the local URL shown in the terminal (usually `http://localhost:8501`).

## Notes

- The app stores employee data in `data/employees.csv` and creates sample data if none exists.
- If you use GitHub, add `.venv/` to `.gitignore` to avoid committing dependencies.
