
import pandas as pd
import os

DATA_FILE = "data/employees.csv"

DEPARTMENTS = ["HR", "Engineering", "Sales", "Marketing", "Finance", 
               "Operations", "IT", "Support", "Management", "Legal"]

PERFORMANCE_LABELS = {1: "Low", 2: "Average", 3: "High"}

def load_data():
    """Load employee data from CSV, create sample if not exists."""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(DATA_FILE):
        _create_sample_data()
    
    df = pd.read_csv(DATA_FILE)
    # Ensure correct types
    numeric_cols = ["id", "age", "years_experience", "salary", 
                    "attendance_score", "training_hours", "projects_completed", "performance_level"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

def save_data(df):
    """Save dataframe to CSV."""
    if not os.path.exists("data"):
        os.makedirs("data")
    df.to_csv(DATA_FILE, index=False)

def get_next_id(df):
    if df.empty:
        return 1
    return int(df["id"].max()) + 1

def add_employee(df, employee_data):
    new_id = get_next_id(df)
    employee_data["id"] = new_id
    new_row = pd.DataFrame([employee_data])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    return df, new_id

def update_employee(df, emp_id, updated_data):
    idx = df[df["id"] == emp_id].index
    if len(idx) == 0:
        return df, False
    for key, val in updated_data.items():
        df.at[idx[0], key] = val
    save_data(df)
    return df, True

def delete_employee(df, emp_id):
    df = df[df["id"] != emp_id].reset_index(drop=True)
    save_data(df)
    return df

def search_employees(df, query, field="name"):
    if not query:
        return df
    return df[df[field].astype(str).str.lower().str.contains(query.lower())]

def import_csv(uploaded_file):
    """Import employees from uploaded CSV."""
    imported = pd.read_csv(uploaded_file)
    # Validate required columns
    required = ["name", "email", "department", "salary"]
    missing = [c for c in required if c not in imported.columns]
    if missing:
        return None, f"Missing required columns: {', '.join(missing)}"
    
    existing = load_data()
    # Re-index IDs
    start_id = get_next_id(existing)
    imported["id"] = range(start_id, start_id + len(imported))
    
    combined = pd.concat([existing, imported], ignore_index=True)
    save_data(combined)
    return combined, None

def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def _create_sample_data():
    """Create sample employees.csv from provided data."""
    sample = pd.DataFrame([
        {"id": 1, "name": "Alice", "email": "alice.hr@example.com", "contact": "555-0101", "age": 28, "department": "HR", "years_experience": 3, "salary": 38000, "attendance_score": 85, "training_hours": 20, "projects_completed": 1, "performance_level": 2},
        {"id": 2, "name": "Bob", "email": "bob.eng@example.com", "contact": "555-0102", "age": 35, "department": "Engineering", "years_experience": 10, "salary": 90000, "attendance_score": 92, "training_hours": 40, "projects_completed": 8, "performance_level": 3},
        {"id": 3, "name": "Carol", "email": "carol.sales@example.com", "contact": "555-0103", "age": 24, "department": "Sales", "years_experience": 1, "salary": 32000, "attendance_score": 72, "training_hours": 10, "projects_completed": 2, "performance_level": 1},
        {"id": 4, "name": "David", "email": "david.marketing@example.com", "contact": "555-0104", "age": 29, "department": "Marketing", "years_experience": 6, "salary": 56000, "attendance_score": 88, "training_hours": 25, "projects_completed": 5, "performance_level": 2},
        {"id": 5, "name": "Emily", "email": "emily.finance@example.com", "contact": "555-0105", "age": 42, "department": "Finance", "years_experience": 18, "salary": 120000, "attendance_score": 95, "training_hours": 55, "projects_completed": 20, "performance_level": 3},
        {"id": 6, "name": "Frank", "email": "frank.ops@example.com", "contact": "555-0106", "age": 31, "department": "Operations", "years_experience": 8, "salary": 68000, "attendance_score": 80, "training_hours": 30, "projects_completed": 6, "performance_level": 2},
        {"id": 7, "name": "Grace", "email": "grace.it@example.com", "contact": "555-0107", "age": 26, "department": "IT", "years_experience": 2, "salary": 47000, "attendance_score": 78, "training_hours": 18, "projects_completed": 3, "performance_level": 2},
        {"id": 8, "name": "Henry", "email": "henry.support@example.com", "contact": "555-0108", "age": 23, "department": "Support", "years_experience": 1, "salary": 30000, "attendance_score": 65, "training_hours": 8, "projects_completed": 1, "performance_level": 1},
        {"id": 9, "name": "Irene", "email": "irene.management@example.com", "contact": "555-0109", "age": 45, "department": "Management", "years_experience": 22, "salary": 140000, "attendance_score": 97, "training_hours": 60, "projects_completed": 30, "performance_level": 3},
        {"id": 10, "name": "Jack", "email": "jack.eng@example.com", "contact": "555-0110", "age": 39, "department": "Engineering", "years_experience": 15, "salary": 110000, "attendance_score": 90, "training_hours": 45, "projects_completed": 15, "performance_level": 3},
        {"id": 11, "name": "Karen", "email": "karen.hr@example.com", "contact": "555-0111", "age": 33, "department": "HR", "years_experience": 7, "salary": 52000, "attendance_score": 84, "training_hours": 22, "projects_completed": 4, "performance_level": 2},
        {"id": 12, "name": "Liam", "email": "liam.sales@example.com", "contact": "555-0112", "age": 27, "department": "Sales", "years_experience": 4, "salary": 44000, "attendance_score": 70, "training_hours": 15, "projects_completed": 3, "performance_level": 1},
        {"id": 13, "name": "Mia", "email": "mia.finance@example.com", "contact": "555-0113", "age": 38, "department": "Finance", "years_experience": 12, "salary": 95000, "attendance_score": 91, "training_hours": 48, "projects_completed": 12, "performance_level": 3},
        {"id": 14, "name": "Noah", "email": "noah.it@example.com", "contact": "555-0114", "age": 30, "department": "IT", "years_experience": 5, "salary": 62000, "attendance_score": 82, "training_hours": 28, "projects_completed": 7, "performance_level": 2},
        {"id": 15, "name": "Olivia", "email": "olivia.marketing@example.com", "contact": "555-0115", "age": 25, "department": "Marketing", "years_experience": 2, "salary": 39000, "attendance_score": 76, "training_hours": 14, "projects_completed": 2, "performance_level": 1},
        {"id": 16, "name": "Paul", "email": "paul.ops@example.com", "contact": "555-0116", "age": 44, "department": "Operations", "years_experience": 20, "salary": 105000, "attendance_score": 93, "training_hours": 50, "projects_completed": 18, "performance_level": 3},
        {"id": 17, "name": "Quinn", "email": "quinn.support@example.com", "contact": "555-0117", "age": 22, "department": "Support", "years_experience": 1, "salary": 28000, "attendance_score": 60, "training_hours": 6, "projects_completed": 1, "performance_level": 1},
        {"id": 18, "name": "Rachel", "email": "rachel.eng@example.com", "contact": "555-0118", "age": 36, "department": "Engineering", "years_experience": 11, "salary": 98000, "attendance_score": 89, "training_hours": 42, "projects_completed": 10, "performance_level": 3},
        {"id": 19, "name": "Sam", "email": "sam.management@example.com", "contact": "555-0119", "age": 50, "department": "Management", "years_experience": 25, "salary": 160000, "attendance_score": 96, "training_hours": 65, "projects_completed": 35, "performance_level": 3},
        {"id": 20, "name": "Tina", "email": "tina.hr@example.com", "contact": "555-0120", "age": 32, "department": "HR", "years_experience": 9, "salary": 58000, "attendance_score": 83, "training_hours": 32, "projects_completed": 6, "performance_level": 2},
    ])
    if not os.path.exists("data"):
        os.makedirs("data")
    sample.to_csv(DATA_FILE, index=False)