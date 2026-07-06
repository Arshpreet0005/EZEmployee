
import streamlit as st
import pandas as pd
from modules import data_manager

def render(df):
    st.markdown("""
    <div class="page-header">
        <p class="page-title">👤 Employee Management</p>
        <p class="page-subtitle">Add, view, search, update, and delete employee records</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📋 View & Search", "➕ Add Employee", "✏️ Update Employee", "🗑️ Delete Employee", "📥 Import / Export"])

    with tabs[0]:
        _view_search(df)
    with tabs[1]:
        df = _add_employee(df)
    with tabs[2]:
        df = _update_employee(df)
    with tabs[3]:
        df = _delete_employee(df)
    with tabs[4]:
        _import_export(df)

    return df


def _view_search(df):
    st.markdown("#### Search & Filter Employees")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search by name or email", placeholder="e.g. Alice")
    with col2:
        dept_filter = st.selectbox("Department", ["All"] + sorted(df["department"].unique().tolist()))
    with col3:
        perf_filter = st.selectbox("Performance", ["All", "High (3)", "Average (2)", "Low (1)"])

    filtered = df.copy()
    if search_query:
        mask = (
            df["name"].str.lower().str.contains(search_query.lower()) |
            df["email"].str.lower().str.contains(search_query.lower())
        )
        filtered = filtered[mask]
    if dept_filter != "All":
        filtered = filtered[filtered["department"] == dept_filter]
    if perf_filter != "All":
        level = int(perf_filter.split("(")[1].replace(")", ""))
        filtered = filtered[filtered["performance_level"] == level]

    st.markdown(f"**Showing {len(filtered)} employees**")

    perf_map = {1: "🔴 Low", 2: "🟡 Average", 3: "🟢 High"}
    display_df = filtered.copy()
    display_df["performance_level"] = display_df["performance_level"].map(perf_map)
    display_df["salary"] = display_df["salary"].apply(lambda x: f"${x:,.0f}")

    st.dataframe(
        display_df[["id", "name", "email", "contact", "department", "age",
                    "years_experience", "salary", "attendance_score",
                    "training_hours", "projects_completed", "performance_level"]].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )


def _add_employee(df):
    st.markdown("#### Add New Employee")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            contact = st.text_input("Contact Number")
            age = st.number_input("Age", min_value=18, max_value=70, value=25)
            department = st.selectbox("Department *", data_manager.DEPARTMENTS)
        with col2:
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, value=1)
            salary = st.number_input("Salary ($)", min_value=10000, max_value=500000, value=40000, step=1000)
            attendance = st.slider("Attendance Score (%)", 0, 100, 80)
            training_hrs = st.number_input("Training Hours", min_value=0, max_value=200, value=20)
            projects = st.number_input("Projects Completed", min_value=0, max_value=100, value=1)
            performance = st.selectbox("Performance Level", [1, 2, 3],
                                       format_func=lambda x: {1: "1 - Low", 2: "2 - Average", 3: "3 - High"}[x])

        submitted = st.form_submit_button("➕ Add Employee", use_container_width=True)
        
        if submitted:
            if not name or not email:
                st.error("Name and Email are required!")
            elif email in df["email"].values:
                st.error(f"Email '{email}' already exists!")
            else:
                emp_data = {
                    "name": name, "email": email, "contact": contact,
                    "age": age, "department": department,
                    "years_experience": years_exp, "salary": salary,
                    "attendance_score": attendance, "training_hours": training_hrs,
                    "projects_completed": projects, "performance_level": performance
                }
                df, new_id = data_manager.add_employee(df, emp_data)
                st.success(f"✅ Employee '{name}' added successfully with ID #{new_id}")
                st.rerun()
    return df


def _update_employee(df):
    st.markdown("#### Update Employee Record")
    
    if df.empty:
        st.info("No employees to update.")
        return df

    emp_options = {f"#{row['id']} — {row['name']}": row["id"] for _, row in df.iterrows()}
    selected = st.selectbox("Select Employee to Update", list(emp_options.keys()))
    emp_id = emp_options[selected]
    emp = df[df["id"] == emp_id].iloc[0]

    with st.form("update_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=str(emp["name"]))
            email = st.text_input("Email", value=str(emp["email"]))
            contact = st.text_input("Contact", value=str(emp.get("contact", "")))
            age = st.number_input("Age", min_value=18, max_value=70, value=int(emp["age"]))
            department = st.selectbox("Department", data_manager.DEPARTMENTS,
                                      index=data_manager.DEPARTMENTS.index(emp["department"]) if emp["department"] in data_manager.DEPARTMENTS else 0)
        with col2:
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, value=int(emp["years_experience"]))
            salary = st.number_input("Salary ($)", min_value=10000, max_value=500000, value=int(emp["salary"]), step=1000)
            attendance = st.slider("Attendance Score (%)", 0, 100, int(emp["attendance_score"]))
            training_hrs = st.number_input("Training Hours", min_value=0, max_value=200, value=int(emp["training_hours"]))
            projects = st.number_input("Projects Completed", min_value=0, max_value=100, value=int(emp["projects_completed"]))
            performance = st.selectbox("Performance Level", [1, 2, 3],
                                       index=int(emp["performance_level"]) - 1,
                                       format_func=lambda x: {1: "1 - Low", 2: "2 - Average", 3: "3 - High"}[x])

        submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
        if submitted:
            updated = {
                "name": name, "email": email, "contact": contact, "age": age,
                "department": department, "years_experience": years_exp,
                "salary": salary, "attendance_score": attendance,
                "training_hours": training_hrs, "projects_completed": projects,
                "performance_level": performance
            }
            df, success = data_manager.update_employee(df, emp_id, updated)
            if success:
                st.success(f"✅ Employee #{emp_id} updated successfully!")
                st.rerun()
            else:
                st.error("Update failed. Employee not found.")
    return df


def _delete_employee(df):
    st.markdown("#### Delete Employee Record")
    
    if df.empty:
        st.info("No employees to delete.")
        return df

    emp_options = {f"#{row['id']} — {row['name']} ({row['department']})": row["id"] for _, row in df.iterrows()}
    selected = st.selectbox("Select Employee to Delete", list(emp_options.keys()))
    emp_id = emp_options[selected]
    emp = df[df["id"] == emp_id].iloc[0]

    st.markdown(f"""
    <div class="alert-medium">
        <strong>⚠️ You are about to delete:</strong><br>
        Name: {emp['name']} | Email: {emp['email']} | Department: {emp['department']}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        confirm = st.checkbox("I confirm deletion")
    if confirm:
        if st.button("🗑️ Delete Employee", type="primary"):
            df = data_manager.delete_employee(df, emp_id)
            st.success(f"✅ Employee #{emp_id} deleted successfully.")
            st.rerun()
    return df


def _import_export(df):
    st.markdown("#### Import & Export CSV")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📥 Import from CSV**")
        st.caption("CSV must contain: name, email, department, salary")
        uploaded = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded:
            new_df, err = data_manager.import_csv(uploaded)
            if err:
                st.error(f"Import failed: {err}")
            else:
                added = len(new_df) - len(df)
                st.success(f"✅ Successfully imported {added} new employees!")
                st.rerun()

    with col2:
        st.markdown("**📤 Export to CSV**")
        st.caption("Download all employee records as CSV")
        csv_data = data_manager.export_csv(df)
        st.download_button(
            label="⬇️ Download employees.csv",
            data=csv_data,
            file_name="employees_export.csv",
            mime="text/csv",
            use_container_width=True
        )