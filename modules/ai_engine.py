
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings("ignore")

FEATURES = ["age", "years_experience", "salary", "attendance_score",
            "training_hours", "projects_completed"]


def _chart_layout(title):
    return dict(
        paper_bgcolor="#F8FAFC",
        plot_bgcolor="#F8FAFC",
        font_family="Inter",
        font_color="#0F172A",
        title=dict(text=title, font=dict(size=13, color="#0F172A")),
        legend=dict(font=dict(color="#0F172A")),
        coloraxis_showscale=False,
        margin=dict(l=5, r=5, t=40, b=5),
    )


def _field_label(text):
    st.markdown(
        f'<div style="font-size:0.95rem;font-weight:700;color:#F8FAFC;margin:0 0 6px 2px;line-height:1.2;">{text}</div>',
        unsafe_allow_html=True,
    )


def _helper_text(text):
    st.markdown(
        f'<div style="font-size:0.9rem;color:#CBD5E1;line-height:1.5;margin:0 0 10px 0;">{text}</div>',
        unsafe_allow_html=True,
    )

# ── helpers ──────────────────────────────────────────────────────────────────

def _get_features(df):
    return df[FEATURES].dropna()

def _train_performance_model(df):
    X = df[FEATURES]
    y = df["performance_level"]
    if len(df) < 5:
        return None, 0
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test)) if len(X_test) > 0 else 1.0
    return clf, round(acc * 100, 1)

def _compute_attrition_risk(df):
    """
    Rule-based attrition score (0–100):
    - Low attendance → high risk
    - Low salary vs peers → higher risk
    - Low performance → higher risk
    - Low training hours → higher risk
    """
    scores = []
    avg_salary = df["salary"].mean()
    for _, row in df.iterrows():
        score = 0
        score += max(0, (70 - row["attendance_score"]) * 1.2)  # low attendance
        if row["salary"] < avg_salary * 0.7:
            score += 25
        elif row["salary"] < avg_salary * 0.85:
            score += 10
        if row["performance_level"] == 1:
            score += 20
        elif row["performance_level"] == 2:
            score += 5
        if row["training_hours"] < 15:
            score += 15
        elif row["training_hours"] < 25:
            score += 5
        if row["years_experience"] < 2:
            score += 10
        scores.append(min(100, score))
    return scores

def _cluster_employees(df, n_clusters=3):
    X = df[FEATURES].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    return labels

# ── render ────────────────────────────────────────────────────────────────────

def render(df):
    st.markdown("""
    <div class="page-header">
        <p class="page-title">🤖 AI Analytics</p>
        <p class="page-subtitle">Machine-learning powered performance prediction, attrition risk & clustering</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df) < 5:
        st.warning("Need at least 5 employees for AI analysis. Add more records first.")
        return

    tabs = st.tabs(["🎯 Performance Predictor", "⚠️ Attrition Risk", "🔵 Employee Clustering"])

    with tabs[0]:
        _performance_tab(df)
    with tabs[1]:
        _attrition_tab(df)
    with tabs[2]:
        _clustering_tab(df)


def _performance_tab(df):
    st.markdown("### 🎯 Performance Level Predictor")
    _helper_text("Random Forest model trained on your employee data to predict performance level (Low / Average / High)")
    _helper_text("Input features: Age, Years Experience, Salary, Attendance Score, Training Hours, Projects Completed")

    # Train model
    with st.spinner("Training model..."):
        model, acc = _train_performance_model(df)

    col_info, col_form = st.columns([1, 2])

    with col_info:
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="metric-value">{acc}%</div>
            <div class="metric-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

        # Feature importance
        importances = model.feature_importances_
        fi_df = pd.DataFrame({"Feature": FEATURES, "Importance": importances})
        fi_df = fi_df.sort_values("Importance", ascending=True)
        fig = px.bar(fi_df, x="Importance", y="Feature", orientation="h",
                     title="Feature Importance", color="Importance",
                     color_continuous_scale=["#DBEAFE", "#1D4ED8"], template="simple_white")
        fig.update_layout(
            **_chart_layout("Feature Importance"),
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A", size=12), title_font=dict(color="#0F172A")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#0F172A", size=12), title_font=dict(color="#0F172A")),
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col_form:
        st.markdown("#### Predict for a New Employee")
        c1, c2 = st.columns(2)
        with c1:
            _field_label("Age")
            p_age = st.number_input("Age", 18, 70, 30, key="p_age", label_visibility="collapsed")
            _field_label("Years Experience")
            p_exp = st.number_input("Years Experience", 0, 50, 5, key="p_exp", label_visibility="collapsed")
            _field_label("Salary ($)")
            p_salary = st.number_input("Salary ($)", 10000, 500000, 60000, 1000, key="p_sal", label_visibility="collapsed")
        with c2:
            _field_label("Attendance Score (%)")
            p_att = st.slider("Attendance Score (%)", 0, 100, 85, key="p_att", label_visibility="collapsed")
            _field_label("Training Hours")
            p_train = st.number_input("Training Hours", 0, 200, 30, key="p_train", label_visibility="collapsed")
            _field_label("Projects Completed")
            p_proj = st.number_input("Projects Completed", 0, 100, 5, key="p_proj", label_visibility="collapsed")

        if st.button("🔮 Predict Performance", use_container_width=True):
            input_df = pd.DataFrame([{
                "age": p_age, "years_experience": p_exp, "salary": p_salary,
                "attendance_score": p_att, "training_hours": p_train, "projects_completed": p_proj
            }])
            pred = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0]
            classes = model.classes_

            label_map = {1: "🔴 Low", 2: "🟡 Average", 3: "🟢 High"}
            color_map = {1: "alert-high", 2: "alert-medium", 3: "alert-low"}

            st.markdown(f"""
            <div class="{color_map[pred]}">
                <strong>Predicted Performance Level: {label_map[pred]}</strong>
            </div>
            """, unsafe_allow_html=True)

            # Probability bars
            st.markdown("**Confidence Breakdown:**")
            for cls, prob in zip(classes, proba):
                st.progress(float(prob), text=f"{label_map[cls]}: {prob*100:.1f}%")

    st.markdown("---")
    st.markdown("#### Batch Predictions for All Employees")
    if model:
        X_all = df[FEATURES]
        preds = model.predict(X_all)
        probas = model.predict_proba(X_all)
        label_map = {1: "Low", 2: "Average", 3: "High"}
        pred_df = df[["id", "name", "department", "performance_level"]].copy()
        pred_df["predicted"] = preds
        pred_df["actual"] = pred_df["performance_level"].map(label_map)
        pred_df["predicted_label"] = pred_df["predicted"].map(label_map)
        pred_df["confidence"] = [f"{max(p)*100:.1f}%" for p in probas]
        pred_df["match"] = pred_df["performance_level"] == pred_df["predicted"]
        pred_df["match"] = pred_df["match"].map({True: "✅", False: "❌"})
        st.dataframe(
            pred_df[["id", "name", "department", "actual", "predicted_label", "confidence", "match"]],
            use_container_width=True, hide_index=True
        )


def _attrition_tab(df):
    st.markdown("### ⚠️ Attrition Risk Scoring")
    st.caption("Rule-based AI model that identifies employees at risk of leaving based on salary, performance, attendance & training")

    risk_scores = _compute_attrition_risk(df)
    risk_df = df[["id", "name", "department", "salary", "attendance_score",
                  "performance_level", "training_hours", "years_experience"]].copy()
    risk_df["attrition_risk"] = risk_scores

    def risk_label(score):
        if score >= 50: return "High"
        elif score >= 25: return "Medium"
        return "Low"

    risk_df["risk_level"] = risk_df["attrition_risk"].apply(risk_label)

    # Summary
    high = len(risk_df[risk_df["risk_level"] == "High"])
    medium = len(risk_df[risk_df["risk_level"] == "Medium"])
    low = len(risk_df[risk_df["risk_level"] == "Low"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card red">
            <div class="metric-value">{high}</div>
            <div class="metric-label">High Risk Employees</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-value">{medium}</div>
            <div class="metric-label">Medium Risk Employees</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-value">{low}</div>
            <div class="metric-label">Low Risk Employees</div>
        </div>
        """, unsafe_allow_html=True)

    # Visuals
    col1, col2 = st.columns(2)

    with col1:
        color_map = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
        fig = px.bar(
            risk_df.sort_values("attrition_risk", ascending=False),
            x="name", y="attrition_risk", color="risk_level",
            color_discrete_map=color_map, title="Attrition Risk Score per Employee",
            labels={"attrition_risk": "Risk Score", "name": "Employee"},
            template="simple_white"
        )
        fig.update_layout(
            **_chart_layout("Attrition Risk Score per Employee"),
            xaxis=dict(tickangle=-45, showgrid=False, tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dept_risk = risk_df.groupby("department")["attrition_risk"].mean().reset_index()
        dept_risk.columns = ["Department", "Avg Risk"]
        dept_risk = dept_risk.sort_values("Avg Risk", ascending=False)
        fig2 = px.bar(
            dept_risk, x="Avg Risk", y="Department", orientation="h",
            color="Avg Risk", color_continuous_scale=["#D1FAE5", "#EF4444"],
            title="Avg Attrition Risk by Department",
            template="simple_white"
        )
        fig2.update_layout(
            **_chart_layout("Avg Attrition Risk by Department"),
            showlegend=False,
            xaxis=dict(tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
            yaxis=dict(tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # High-risk alerts
    if high > 0:
        st.markdown("#### 🚨 High-Risk Employees — Immediate HR Attention Needed")
        high_risk_emp = risk_df[risk_df["risk_level"] == "High"].sort_values("attrition_risk", ascending=False)
        for _, row in high_risk_emp.iterrows():
            reasons = []
            if row["attendance_score"] < 70: reasons.append("Low attendance")
            if row["salary"] < risk_df["salary"].mean() * 0.75: reasons.append("Below-avg salary")
            if row["performance_level"] == 1: reasons.append("Low performance")
            if row["training_hours"] < 15: reasons.append("Insufficient training")
            st.markdown(f"""
            <div class="alert-high">
                <strong>{row['name']}</strong> (#{int(row['id'])}) — {row['department']} — 
                Risk Score: <strong>{row['attrition_risk']:.0f}/100</strong><br>
                <small>⚡ Reasons: {', '.join(reasons) if reasons else 'Multiple combined factors'}</small>
            </div>
            """, unsafe_allow_html=True)

    # Full table
    st.markdown("#### Full Risk Assessment Table")
    display = risk_df.copy()
    display["attrition_risk"] = display["attrition_risk"].apply(lambda x: f"{x:.1f}")
    st.dataframe(
        display[["id", "name", "department", "attrition_risk", "risk_level",
                 "attendance_score", "salary", "training_hours"]].sort_values("risk_level"),
        use_container_width=True, hide_index=True
    )


def _clustering_tab(df):
    st.markdown("### 🔵 Employee Clustering (K-Means)")
    st.caption("Unsupervised ML groups employees into similar profiles based on experience, salary, performance & training")

    col_ctrl, _ = st.columns([1, 3])
    with col_ctrl:
        n_clusters = st.slider("Number of Clusters", 2, 6, 3)

    with st.spinner("Clustering employees..."):
        labels = _cluster_employees(df, n_clusters)

    cluster_df = df.copy()
    cluster_df["cluster"] = [f"Group {l+1}" for l in labels]

    # Scatter: experience vs salary
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(
            cluster_df, x="years_experience", y="salary",
            color="cluster", size="projects_completed",
            title="Clusters: Experience vs Salary",
            labels={"years_experience": "Years Exp", "salary": "Salary"},
            hover_data=["name", "department"],
            template="simple_white"
        )
        fig.update_layout(
            **_chart_layout("Clusters: Experience vs Salary"),
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            cluster_df, x="attendance_score", y="training_hours",
            color="cluster", size="salary",
            title="Clusters: Attendance vs Training",
            labels={"attendance_score": "Attendance %", "training_hours": "Training Hrs"},
            hover_data=["name", "department"],
            template="simple_white"
        )
        fig2.update_layout(
            **_chart_layout("Clusters: Attendance vs Training"),
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Cluster profiles
    st.markdown("#### Cluster Profiles (Average Metrics)")
    profile = cluster_df.groupby("cluster")[FEATURES + ["performance_level"]].mean().round(1)
    profile["count"] = cluster_df.groupby("cluster")["id"].count()
    st.dataframe(profile, use_container_width=True)

    # Per-cluster breakdown
    st.markdown("#### Employees per Cluster")
    for g in sorted(cluster_df["cluster"].unique()):
        grp = cluster_df[cluster_df["cluster"] == g]
        with st.expander(f"{g} — {len(grp)} employees"):
            st.dataframe(
                grp[["id", "name", "department", "salary", "years_experience",
                     "performance_level", "attendance_score"]].reset_index(drop=True),
                use_container_width=True, hide_index=True
            )

    # HR insights per cluster
    st.markdown("#### 💡 AI-Generated Cluster Insights")
    for g in sorted(cluster_df["cluster"].unique()):
        grp = cluster_df[cluster_df["cluster"] == g]
        avg_sal = grp["salary"].mean()
        avg_perf = grp["performance_level"].mean()
        avg_att = grp["attendance_score"].mean()
        avg_exp = grp["years_experience"].mean()

        if avg_perf >= 2.5 and avg_sal >= cluster_df["salary"].mean():
            tag, insight = "🟢 Star Performers", "Top talent — consider retention bonuses and leadership development."
        elif avg_perf <= 1.5 or avg_att < 75:
            tag, insight = "🔴 Needs Support", "Performance or attendance concerns — initiate coaching and training plans."
        else:
            tag, insight = "🟡 Core Workforce", "Stable contributors — maintain engagement with training and recognition."

        st.markdown(f"""
        <div class="section-card">
            <strong>{g}: {tag}</strong><br>
            <small>Avg Salary: ${avg_sal:,.0f} | Avg Perf: {avg_perf:.1f}/3 | Avg Attendance: {avg_att:.1f}% | Avg Exp: {avg_exp:.1f} yrs</small><br>
            <p style="margin-top:8px; color: #374151;">💡 {insight}</p>
        </div>
        """, unsafe_allow_html=True)