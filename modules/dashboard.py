
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def _dark_chart_layout(title, height=None):
    layout = dict(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font_family="Inter",
        font_color="#E2E8F0",
        title=dict(text=title, font=dict(size=14, color="#F8FAFC")),
        legend=dict(font=dict(color="#E2E8F0")),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    if height is not None:
        layout["height"] = height
    return layout

def render(df):
    st.markdown("""
    <div class="page-header">
        <p class="page-title">📊 HR Dashboard</p>
        <p class="page-subtitle">Real-time overview of your workforce analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No employee data found. Add employees to see the dashboard.")
        return

    total = len(df)
    avg_salary = df["salary"].mean()
    avg_attendance = df["attendance_score"].mean()
    high_performers = len(df[df["performance_level"] == 3])

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total}</div>
            <div class="metric-label">Total Employees</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-value">${avg_salary:,.0f}</div>
            <div class="metric-label">Avg. Salary</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-value">{avg_attendance:.1f}%</div>
            <div class="metric-label">Avg. Attendance</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        pct = (high_performers / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div class="metric-card purple">
            <div class="metric-value">{high_performers}</div>
            <div class="metric-label">High Performers ({pct:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Dept distribution + Performance breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        dept_counts = df["department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        fig = px.bar(
            dept_counts, x="Count", y="Department", orientation="h",
            color="Count", color_continuous_scale=["#DBEAFE", "#2563EB"],
            title="Employees by Department",
            template="simple_white"
        )
        fig.update_layout(
            **_dark_chart_layout("Employees by Department"),
            showlegend=False,
            yaxis=dict(showgrid=False, tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0"))
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        perf_map = {1: "Low", 2: "Average", 3: "High"}
        perf_df = df["performance_level"].map(perf_map).value_counts().reset_index()
        perf_df.columns = ["Performance", "Count"]
        colors = {"High": "#10B981", "Average": "#F59E0B", "Low": "#EF4444"}
        fig2 = px.pie(
            perf_df, names="Performance", values="Count",
            title="Performance Distribution",
            color="Performance", color_discrete_map=colors,
            hole=0.45,
            template="simple_white"
        )
        fig2.update_layout(
            **_dark_chart_layout("Performance Distribution")
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

    # Row 3: Salary by dept + Experience vs Salary scatter
    col3, col4 = st.columns(2)

    with col3:
        sal_dept = df.groupby("department")["salary"].mean().reset_index()
        sal_dept.columns = ["Department", "Avg Salary"]
        sal_dept = sal_dept.sort_values("Avg Salary", ascending=False)
        fig3 = px.bar(
            sal_dept, x="Department", y="Avg Salary",
            title="Avg Salary by Department",
            color="Avg Salary", color_continuous_scale=["#EFF6FF", "#1D4ED8"],
            template="simple_white"
        )
        fig3.update_layout(
            **_dark_chart_layout("Avg Salary by Department"),
            showlegend=False,
            xaxis=dict(tickangle=-30, showgrid=False, tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
            yaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0"))
        )
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        perf_label = df["performance_level"].map(perf_map)
        fig4 = px.scatter(
            df, x="years_experience", y="salary",
            color=perf_label, size="projects_completed",
            title="Experience vs Salary (sized by Projects)",
            color_discrete_map={"High": "#10B981", "Average": "#F59E0B", "Low": "#EF4444"},
            labels={"years_experience": "Years Experience", "salary": "Salary", "color": "Performance"},
            template="simple_white"
        )
        fig4.update_layout(
            **_dark_chart_layout("Experience vs Salary (sized by Projects)"),
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
            yaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0"))
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Training hours heatmap by dept
    st.markdown("---")
    st.markdown("#### 📈 Training Hours & Attendance by Department")
    dept_stats = df.groupby("department").agg(
        avg_training=("training_hours", "mean"),
        avg_attendance=("attendance_score", "mean"),
        count=("id", "count")
    ).reset_index()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        name="Avg Training Hours", x=dept_stats["department"],
        y=dept_stats["avg_training"], marker_color="#93C5FD", yaxis="y"
    ))
    fig5.add_trace(go.Scatter(
        name="Avg Attendance %", x=dept_stats["department"],
        y=dept_stats["avg_attendance"], mode="lines+markers",
        marker=dict(color="#2563EB", size=8),
        line=dict(color="#2563EB", width=2), yaxis="y2"
    ))
    fig5.update_layout(
        paper_bgcolor="#0F172A", plot_bgcolor="#0F172A",
        font_family="Inter", font_color="#E2E8F0", margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(title="Training Hours", showgrid=True, gridcolor="#334155", tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
        yaxis2=dict(title="Attendance %", overlaying="y", side="right", range=[50, 100], tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
        xaxis=dict(showgrid=False, tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#E2E8F0")),
        barmode="group"
    )
    st.plotly_chart(fig5, use_container_width=True)