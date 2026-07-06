
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from modules import data_manager

def render(df):
    st.markdown("""
    <div class="page-header">
        <p class="page-title">📊 Reports & Exports</p>
        <p class="page-subtitle">Generate HR summaries, download data, and view workforce statistics</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No data available to generate reports.")
        return

    tabs = st.tabs(["📄 HR Summary", "💰 Salary Analysis", "📈 Performance Report", "⬇️ Export Data"])

    with tabs[0]:
        _hr_summary(df)
    with tabs[1]:
        _salary_analysis(df)
    with tabs[2]:
        _performance_report(df)
    with tabs[3]:
        _export_data(df)


def _hr_summary(df):
    st.markdown("### 📄 HR Summary Report")

    total = len(df)
    dept_count = df["department"].nunique()
    avg_age = df["age"].mean()
    avg_exp = df["years_experience"].mean()
    avg_salary = df["salary"].mean()
    avg_attend = df["attendance_score"].mean()

    perf_map = {1: "Low", 2: "Average", 3: "High"}

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total}</div>
            <div class="metric-label">Total Employees</div>
        </div>
        <div class="metric-card green">
            <div class="metric-value">{dept_count}</div>
            <div class="metric-label">Departments</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">Avg Employee Age</div>
        </div>
        <div class="metric-card purple">
            <div class="metric-value">{avg_exp:.1f} yrs</div>
            <div class="metric-label">Avg Experience</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-value">${avg_salary:,.0f}</div>
            <div class="metric-label">Avg Salary</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{avg_attend:.1f}%</div>
            <div class="metric-label">Avg Attendance</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Department Breakdown")
    dept_summary = df.groupby("department").agg(
        Employees=("id", "count"),
        Avg_Salary=("salary", "mean"),
        Avg_Attendance=("attendance_score", "mean"),
        Avg_Experience=("years_experience", "mean"),
        Avg_Training=("training_hours", "mean")
    ).reset_index()
    dept_summary["Avg_Salary"] = dept_summary["Avg_Salary"].apply(lambda x: f"${x:,.0f}")
    dept_summary["Avg_Attendance"] = dept_summary["Avg_Attendance"].apply(lambda x: f"{x:.1f}%")
    dept_summary["Avg_Experience"] = dept_summary["Avg_Experience"].apply(lambda x: f"{x:.1f} yrs")
    dept_summary["Avg_Training"] = dept_summary["Avg_Training"].apply(lambda x: f"{x:.1f} hrs")
    st.dataframe(dept_summary, use_container_width=True, hide_index=True)


def _salary_analysis(df):
    st.markdown("### 💰 Salary Analysis")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(df, x="department", y="salary", color="department",
                     title="Salary Distribution by Department",
                     labels={"salary": "Salary ($)", "department": "Department"})
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                          font_family="Inter", showlegend=False,
                          title_font_size=13, margin=dict(l=5, r=5, t=40, b=5),
                          xaxis=dict(tickangle=-30, showgrid=False),
                          yaxis=dict(showgrid=True, gridcolor="#F1F5F9"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        perf_map = {1: "Low", 2: "Average", 3: "High"}
        df2 = df.copy()
        df2["performance"] = df2["performance_level"].map(perf_map)
        fig2 = px.box(df2, x="performance", y="salary", color="performance",
                      title="Salary Distribution by Performance",
                      color_discrete_map={"High": "#10B981", "Average": "#F59E0B", "Low": "#EF4444"})
        fig2.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                           font_family="Inter", showlegend=False,
                           title_font_size=13, margin=dict(l=5, r=5, t=40, b=5),
                           xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True, gridcolor="#F1F5F9"))
        st.plotly_chart(fig2, use_container_width=True)

    # Salary ranges table
    st.markdown("#### Salary Ranges by Department")
    sal_range = df.groupby("department")["salary"].agg(["min", "max", "mean", "median"]).reset_index()
    sal_range.columns = ["Department", "Min", "Max", "Mean", "Median"]
    for col in ["Min", "Max", "Mean", "Median"]:
        sal_range[col] = sal_range[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(sal_range, use_container_width=True, hide_index=True)


def _performance_report(df):
    st.markdown("### 📈 Performance Report")

    perf_map = {1: "Low", 2: "Average", 3: "High"}
    df2 = df.copy()
    df2["performance"] = df2["performance_level"].map(perf_map)

    col1, col2 = st.columns(2)
    with col1:
        # Performance vs training hours
        fig = px.scatter(df2, x="training_hours", y="projects_completed",
                         color="performance", size="salary",
                         color_discrete_map={"High": "#10B981", "Average": "#F59E0B", "Low": "#EF4444"},
                         title="Training Hours vs Projects Completed",
                         hover_data=["name"])
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                          font_family="Inter", title_font_size=13,
                          margin=dict(l=5, r=5, t=40, b=5),
                          xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
                          yaxis=dict(showgrid=True, gridcolor="#F1F5F9"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dept_perf = df2.groupby(["department", "performance"]).size().reset_index(name="count")
        fig2 = px.bar(dept_perf, x="department", y="count", color="performance",
                      color_discrete_map={"High": "#10B981", "Average": "#F59E0B", "Low": "#EF4444"},
                      title="Performance by Department", barmode="stack")
        fig2.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                           font_family="Inter", title_font_size=13,
                           margin=dict(l=5, r=5, t=40, b=5),
                           xaxis=dict(tickangle=-30, showgrid=False),
                           yaxis=dict(showgrid=True, gridcolor="#F1F5F9"))
        st.plotly_chart(fig2, use_container_width=True)

    # Top performers table
    st.markdown("#### 🏆 Top 5 Performers")
    top = df2[df2["performance_level"] == 3].sort_values("projects_completed", ascending=False).head(5)
    st.dataframe(
        top[["id", "name", "department", "salary", "attendance_score",
             "training_hours", "projects_completed"]].reset_index(drop=True),
        use_container_width=True, hide_index=True
    )


def _export_data(df):
    st.markdown("### ⬇️ Export Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Full Employee CSV**")
        csv = data_manager.export_csv(df)
        st.download_button("⬇️ Download All Employees", csv,
                           "employees_full.csv", "text/csv", use_container_width=True)

    with col2:
        st.markdown("**Filter & Export**")
        dept = st.selectbox("Filter by Department", ["All"] + sorted(df["department"].unique().tolist()), key="exp_dept")
        filtered = df if dept == "All" else df[df["department"] == dept]
        csv2 = data_manager.export_csv(filtered)
        st.download_button(f"⬇️ Download {dept} Employees",
                           csv2, f"employees_{dept.lower()}.csv", "text/csv",
                           use_container_width=True)

    st.markdown("---")
    st.markdown("**Preview of Export Data**")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)