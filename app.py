
import streamlit as st

st.set_page_config(
    page_title="EZEmployee AI",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean professional SaaS look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #0B1220 0%, #111827 40%, #1E293B 100%);
    }
    
    .stApp {
        background: linear-gradient(180deg, #0B1220 0%, #111827 40%, #1E293B 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A5F 0%, #2563EB 100%);
        border-right: none;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.96);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.24);
        border-left: 4px solid #2563EB;
        margin-bottom: 16px;
    }
    
    .metric-card.green { border-left-color: #10B981; }
    .metric-card.orange { border-left-color: #F59E0B; }
    .metric-card.red { border-left-color: #EF4444; }
    .metric-card.purple { border-left-color: #8B5CF6; }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: #CBD5E1;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 6px;
    }
    
    /* Page header */
    .page-header {
        background: rgba(15, 23, 42, 0.94);
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.24);
    }
    
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
    }
    
    .page-subtitle {
        font-size: 0.9rem;
        color: #CBD5E1;
        margin-top: 4px;
    }
    
    /* Section cards */
    .section-card {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
        margin-bottom: 20px;
    }
    
    /* AI Result badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-blue { background: #DBEAFE; color: #1D4ED8; }
    .badge-green { background: #D1FAE5; color: #065F46; }
    .badge-red { background: #FEE2E2; color: #991B1B; }
    .badge-yellow { background: #FEF3C7; color: #92400E; }
    
    /* Sidebar brand */
    .sidebar-brand {
        padding: 16px 0 28px 0;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 20px;
    }
    
    .sidebar-brand h2 {
        color: white !important;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    
    .sidebar-brand p {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.75rem;
        margin: 4px 0 0 0;
    }
    
    /* Hide Streamlit default elements except the header toolbar, which keeps
       the sidebar expand/collapse control available. */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: visible;}
    [data-testid="stToolbar"] {visibility: visible;}
    
    .field-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #E2E8F0;
        margin: 0 0 0.35rem 0;
    }
    
    /* Button styles */
    .stButton > button {
        background: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.92);
        border-radius: 10px;
    }

    /* Tabs and text containers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.72);
        color: #E2E8F0;
        border-radius: 10px;
        padding: 0.6rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background: #2563EB;
        color: white;
    }
    
    /* Alert boxes */
    .alert-high {
        background: #FEE2E2;
        border: 1px solid #FECACA;
        border-radius: 8px;
        padding: 12px 16px;
        color: #991B1B;
        margin: 8px 0;
    }
    
    .alert-medium {
        background: #FEF3C7;
        border: 1px solid #FDE68A;
        border-radius: 8px;
        padding: 12px 16px;
        color: #92400E;
        margin: 8px 0;
    }
    
    .alert-low {
        background: #D1FAE5;
        border: 1px solid #A7F3D0;
        border-radius: 8px;
        padding: 12px 16px;
        color: #065F46;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

from modules import data_manager, employee_crud, ai_engine, dashboard, reports

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <h2>👥 EZEmployee</h2>
            <p>AI-Powered HR Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Navigation**")
        page = st.radio(
            "",
            ["🏠 Dashboard", "👤 Employees", "🤖 AI Analytics", "📊 Reports"],
            label_visibility="collapsed"
        )
        
        return page

def main():
    # Load data
    df = data_manager.load_data()
    
    # Sidebar navigation
    page = render_sidebar()
    
    if page == "🏠 Dashboard":
        dashboard.render(df)
    elif page == "👤 Employees":
        employee_crud.render(df)
    elif page == "🤖 AI Analytics":
        ai_engine.render(df)
    elif page == "📊 Reports":
        reports.render(df)

if __name__ == "__main__":
    main()
