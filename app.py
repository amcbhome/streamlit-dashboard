import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==============================================================================
# 1. PAGE CONFIGURATION & ARCHITECTURE
# ==============================================================================
st.set_page_config(
    page_title="Apex Executive - SaaS Analytics Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Injection for Obsidian/Slate Dark Theme
# Customizing metric cards, background colors, borders, and typography.
st.markdown("""
<style>
    /* Premium dark palette variables */
    :root {
        --bg-primary: #0b0f19;
        --bg-secondary: #111827;
        --border-color: #1f2937;
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --text-primary: #f3f4f6;
        --text-muted: #9ca3af;
    }

    /* Overall Application styling override */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Styling for Streamlit Metric Cards */
    div[data-testid="stMetric"] {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: var(--accent-blue);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15);
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.075em;
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        margin-top: 8px;
    }

    /* Target specific Delta indicator inside metric */
    div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Clean custom navigation styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }

    /* Custom Header Utilities */
    .header-gradient {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .subtitle-muted {
        color: var(--text-muted);
        font-size: 16px;
        margin-top: 4px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. SEEDED HIGH-FIDELITY SYNTHETIC DATA ENGINE
# ==============================================================================
@st.cache_data
def generate_corporate_analytics_data():
    """Generates realistic SaaS historical and demographic records."""
    np.random.seed(42)
    end_date = datetime.now()
    dates = [end_date - timedelta(days=x) for x in range(365)]
    dates.reverse()
    
    # Financial metrics: compound exponential growth with weekly seasonality & noise
    base_mrr = 180000.0
    daily_growth_trend = np.linspace(0, 140000, 365)
    noise = np.random.normal(loc=0, scale=1200, size=365)
    mrr = base_mrr + daily_growth_trend + noise
    
    # Active Users: weekly drop (weekend dips) + dynamic scaling relative to growth
    base_dau = 14200
    weekly_seasonality = np.sin(np.array(range(365)) * (2 * np.pi / 7)) * 1800
    user_growth = np.linspace(0, 28000, 365) + np.random.normal(loc=0, scale=300, size=365)
    dau = (base_dau + weekly_seasonality + user_growth).astype(int)
    
    # Conversion Rate trends: improving slightly as product market fit refines
    base_conv = 2.4
    conv_improvement = np.linspace(0, 1.2, 365) + np.random.normal(loc=0, scale=0.15, size=365)
    conversion_rate = np.clip(base_conv + conv_improvement, 1.0, 5.0)
    
    # Create daily tracking metrics dataframe
    df_daily = pd.DataFrame({
        'Date': dates,
        'MRR': mrr,
        'DAU': dau,
        'ConversionRate': conversion_rate
    })
    
    # Customer Segment Registry
    plans = ['Enterprise Dev', 'Scale Architecture', 'Cloud Starter']
    regions = ['North America', 'EMEA Cluster', 'APAC Expansion', 'LATAM Node']
    industries = ['Fintech', 'Healthcare AI', 'DevOps & Infra', 'Cybersecurity', 'EdTech']
    
    num_customers = 2400
    df_customers = pd.DataFrame({
        'CustomerID': [f"ACC-{i:05d}" for i in range(1, num_customers + 1)],
        'Plan': np.random.choice(plans, size=num_customers, p=[0.20, 0.45, 0.35]),
        'Region': np.random.choice(regions, size=num_customers, p=[0.40, 0.35, 0.15, 0.10]),
        'Industry': np.random.choice(industries, size=num_customers),
        'ContractValue': np.random.choice([12000, 3600, 990], size=num_customers, p=[0.20, 0.45, 0.35]),
        'Status': np.random.choice(['Active', 'Churned'], size=num_customers, p=[0.935, 0.065]),
        'RiskProfile': np.random.choice(['High', 'Medium', 'Low'], size=num_customers, p=[0.12, 0.28, 0.60])
    })
    
    return df_daily, df_customers

# Fetch cached baseline datasets
df_daily, df_customers = generate_corporate_analytics_data()


# ==============================================================================
# 3. INTERACTIVE SIDEBAR & FILTER TOPOLOGY
# ==============================================================================
with st.sidebar:
    # Stylized logo/branding marker
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); width: 44px; height: 44px; border-radius: 10px; display: grid; place-items: center; font-weight: 800; font-size: 22px; color: white;">
                A
            </div>
            <div>
                <h3 style="margin:0; padding:0; color:#f3f4f6; font-size:18px;">Apex Analytics</h3>
                <span style="color:#9ca3af; font-size:12px;">v2.6 Enterprise</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### Operational Controls")
    
    # 1. Date Range Slider filter
    min_date = df_daily['Date'].min()
    max_date = df_daily['Date'].max()
    
    date_filter = st.date_input(
        "Reporting Interval",
        value=(max_date - timedelta(days=90), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # 2. Region Multi-select filter
    available_regions = df_customers['Region'].unique().tolist()
    selected_regions = st.multiselect(
        "Global Infrastructure Node",
        options=available_regions,
        default=available_regions
    )
    
    # 3. Segment Filter dropdown
    available_plans = df_customers['Plan'].unique().tolist()
    selected_plans = st.multiselect(
        "Subscription Tier Access",
        options=available_plans,
        default=available_plans
    )
    
    st.divider()
    
    # System Telemetry Panel
    st.markdown("### Cluster Integrity")
    telemetry_cols = st.columns(2)
    with telemetry_cols[0]:
        st.markdown("<span style='font-size:12px; color:#9ca3af;'>API Gateway</span><br><strong style='color:#10b981;'>● Operational</strong>", unsafe_allow_html=True)
    with telemetry_cols[1]:
        st.markdown("<span style='font-size:12px; color:#9ca3af;'>Sync Latency</span><br><strong style='color:#3b82f6;'>14ms</strong>", unsafe_allow_html=True)

# Application of filtering logic
if len(date_filter) == 2:
    start, end = date_filter
    daily_mask = (df_daily['Date'].dt.date >= start) & (df_daily['Date'].dt.date <= end)
    filtered_daily = df_daily.loc[daily_mask]
else:
    filtered_daily = df_daily

filtered_customers = df_customers[
    (df_customers['Region'].isin(selected_regions)) &
    (df_customers['Plan'].isin(selected_plans))
]


# ==============================================================================
# 4. EXECUTIVE HERO HERO SECTION & KPI GRID
# ==============================================================================
st.markdown("<h1 class='header-gradient'>Apex Corporate Revenue Engine</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-muted'>Real-time SaaS billing metrics, client segmentation structures, and conversion telemetry.</p>", unsafe_allow_html=True)

# Grid Layout: 4 core corporate KPI metric cards
kpi_cols = st.columns(4)

# KPI 1: Monthly Recurring Revenue calculations
cur_mrr = filtered_daily['MRR'].iloc[-1]
prev_mrr = filtered_daily['MRR'].iloc[0]
mrr_pct_change = ((cur_mrr - prev_mrr) / prev_mrr) * 100

# KPI 2: Active User Density calculation
cur_dau = filtered_daily['DAU'].iloc[-1]
prev_dau = filtered_daily['DAU'].iloc[0]
dau_pct_change = ((cur_dau - prev_dau) / prev_dau) * 100

# KPI 3: Contract Value & Client Health
total_acv = filtered_customers['ContractValue'].sum()
avg_acv = filtered_customers['ContractValue'].mean()

# KPI 4: Churn & Pipeline Risk
churn_subset = filtered_customers[filtered_customers['Status'] == 'Churned']
calculated_churn = (len(churn_subset) / len(filtered_customers)) * 100 if len(filtered_customers) > 0 else 0

with kpi_cols[0]:
    st.metric(
        label="Monthly Recurring Revenue",
        value=f"${cur_mrr:,.0f}",
        delta=f"{mrr_pct_change:+.1f}% vs Start"
    )

with kpi_cols[1]:
    st.metric(
        label="Daily Active Users (DAU)",
        value=f"{cur_dau:,}",
        delta=f"{dau_pct_change:+.1f}% vs Start"
    )

with kpi_cols[2]:
    st.metric(
        label="Portfolio ACV Projection",
        value=f"${total_acv:,.0f}",
        delta=f"${avg_acv:,.0f} Avg Account ACV",
        delta_color="normal"
    )

with kpi_cols[3]:
    st.metric(
        label="Customer Churn Index",
        value=f"{calculated_churn:.2f}%",
        delta="-0.38% MoM Improvement",
        delta_color="inverse"
    )

st.write("")


# ==============================================================================
# 5. DATA VISUALIZATION GRID (ROW 1: REVENUE TRENDS & DISPERSION)
# ==============================================================================
vis_row_1_left, vis_row_1_right = st.columns([2, 1])

with vis_row_1_left:
    st.markdown("### Financial Performance & Growth Projections")
    
    # Advanced Multi-Trace Area/Line Trend Plot
    fig_rev = go.Figure()
    
    # MRR Growth Area Curve
    fig_rev.add_trace(go.Scatter(
        x=filtered_daily['Date'],
        y=filtered_daily['MRR'],
        mode='lines',
        name='Actual Monthly Recurring Revenue (MRR)',
        line=dict(color='#3b82f6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.08)'
    ))
    
    # ARR Trend Projection (12x MRR) on dynamic axis
    fig_rev.add_trace(go.Scatter(
        x=filtered_daily['Date'],
        y=filtered_daily['MRR'] * 12,
        mode='lines',
        name='Annualized Run Rate (ARR Proj.)',
        line=dict(color='#10b981', width=1.5, dash='dash')
    ))
    
    fig_rev.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(color='#9ca3af')),
        xaxis=dict(showgrid=True, gridcolor='#1f2937', tickfont=dict(color='#9ca3af')),
        yaxis=dict(showgrid=True, gridcolor='#1f2937', tickprefix="$", tickfont=dict(color='#9ca3af'))
    )
    
    st.plotly_chart(fig_rev, use_container_width=True)

with vis_row_1_right:
    st.markdown("### Contract Volume Split")
    
    # Contract segmentation pie metrics
    tier_grouped = filtered_customers.groupby('Plan')['ContractValue'].sum().reset_index()
    tier_grouped.columns = ['Plan', 'Volume']
    
    fig_pie = px.pie(
        tier_grouped,
        names='Plan',
        values='Volume',
        hole=0.55,
        color_discrete_sequence=['#3b82f6', '#10b981', '#8b5cf6']
    )
    
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color='#9ca3af')),
        showlegend=True
    )
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')
    
    st.plotly_chart(fig_pie, use_container_width=True)


# ==============================================================================
# 6. DATA VISUALIZATION GRID (ROW 2: GEOGRAPHIC DISPERSION & CUSTOMER SEGMENTS)
# ==============================================================================
st.write("")
vis_row_2_left, vis_row_2_right = st.columns([1, 1])

with vis_row_2_left:
    st.markdown("### Regional Account Demographics")
    
    # Horizontal representation of Regional Performance Index
    region_grouped = filtered_customers.groupby(['Region', 'Status']).size().reset_index(name='Accounts')
    
    fig_region = px.bar(
        region_grouped,
        x='Accounts',
        y='Region',
        color='Status',
        orientation='h',
        color_discrete_map={'Active': '#10b981', 'Churned': '#ef4444'},
        barmode='stack'
    )
    
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#9ca3af')),
        xaxis=dict(showgrid=True, gridcolor='#1f2937', tickfont=dict(color='#9ca3af')),
        yaxis=dict(showgrid=False, tickfont=dict(color='#9ca3af'))
    )
    
    st.plotly_chart(fig_region, use_container_width=True)

with vis_row_2_right:
    st.markdown("### Portfolio Risk Profile Distribution")
    
    # TreeMap detailing contract allocation across Industries and associated Risk Status
    fig_tree = px.treemap(
        filtered_customers,
        path=['Industry', 'RiskProfile'],
        values='ContractValue',
        color='RiskProfile',
        color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
    )
    
    fig_tree.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0)
    )
    
    st.plotly_chart(fig_tree, use_container_width=True)


# ==============================================================================
# 7. CORPORATE REGISTRY DATA WORKSHOP
# ==============================================================================
st.divider()
st.markdown("### Client Accounts Master Ledger")

# Interactive search parameters and filtering targeting data workspace
search_col1, search_col2 = st.columns([2, 2])
with search_col1:
    search_query = st.text_input("🔍 Filter Client Profile via Reference, Industry or Plan")
with search_col2:
    status_filter = st.selectbox("Operational Account Status Filter", ["All Statuses", "Active Only", "Churned Only"])

# Table logic filtering
ledger_df = filtered_customers.copy()

if search_query:
    ledger_df = ledger_df[
        ledger_df['CustomerID'].str.contains(search_query, case=False) |
        ledger_df['Industry'].str.contains(search_query, case=False) |
        ledger_df['Plan'].str.contains(search_query, case=False)
    ]

if status_filter == "Active Only":
    ledger_df = ledger_df[ledger_df['Status'] == 'Active']
elif status_filter == "Churned Only":
    ledger_df = ledger_df[ledger_df['Status'] == 'Churned']

st.dataframe(
    ledger_df,
    column_config={
        "ContractValue": st.column_config.NumberColumn("Annual Contract Value (ACV)", format="$%d"),
        "CustomerID": "Account Reference",
        "Plan": "Service Level Agreement",
        "Status": st.column_config.TextColumn("State Descriptor")
    },
    use_container_width=True,
    hide_index=True
)
