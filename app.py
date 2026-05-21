import streamlit as st 
import pandas as pd
import plotly.express as px
from datetime import datetime, date

st.set_page_config(page_title="ScholarQuant: Strategy Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #e1e4e8; }
    [data-testid="stMetricValue"] { font-size: 32px; color: #00e5ff; font-weight: 700; }
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button { background-color: #238636; color: white; border-radius: 8px; width: 100%; border: none; }
    .stDownloadButton>button { background-color: #1f6feb; color: white; border-radius: 8px; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

st.sidebar.title("ScholarQuant")
st.sidebar.caption("Decision Intelligence v1.0")

with st.sidebar.form("input_form", clear_on_submit=True):
    st.write("### Data Ingestion")
    name = st.text_input("Scholarship Identification", placeholder="e.g. STEM Excellence Grant")
    amount = st.number_input("Capital Award ($)", min_value=0, step=500, value=1000)
    labor_hours = st.slider("Estimated Labor Expenditure (Hours)", 0.5, 50.0, 5.0)

    match_profile = st.select_slider(
        "Candidate Match Probability",
        options=["Baseline", "Competitive", "High Probability", "Optimal Match"],
        value="Competitive"
    )
    deadline = st.date_input("Submission Deadline", min_value=date.today())

    weight_map = {"Baseline": 0.15, "Competitive": 0.40, "High Probability": 0.70, "Optimal Match": 0.95}

    if st.form_submit_button("Execute Analysis"):
        if name and amount > 0:
            prob_factor = weight_map[match_profile]
            ev_capital = amount * prob_factor
            hourly_impact = ev_capital / labor_hours
            days_to_deadline = (deadline - date.today()).days

            st.session_state.portfolio.append({
                "Identification": name,
                "Gross Capital": amount,
                "Expected Value": round(ev_capital, 2),
                "Hourly Impact": round(hourly_impact, 2),
                "Match Profile": match_profile,
                "Days Remaining": max(days_to_deadline, 0),
                "Deadline": str(deadline)
            })
            st.rerun()

st.title("ScholarQuant")
st.caption("Quantitative Decision Support for Academic Capital Acquisition")
st.write("---")

if not st.session_state.portfolio:
    st.info("System currently in standby. Please ingest scholarship data via the Strategic Input Panel.")
else:
    df = pd.DataFrame(st.session_state.portfolio)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Gross Capital Pool", f"${df['Gross Capital'].sum():,}")
    kpi2.metric(Adjusted EV Pool", f"${df['Expected Value'].sum():,.0f}", help="Total funding adjusted for match probability.")
    kpi3.metric("Peak Hourly Yield", f"${df['Hourly Impact'].max()}/hr")
    kpi4.metric("Active Assets", len(df))

    st.write("---")

    col_viz, col_status = st.columns([2, 1])

    with col_viz:
        st.subheader("Expected Hourly Yield by Asset")
        fig = px.bar(
            df.sort_values("Hourly Impact"),
            x="Hourly Impact", y="Identification",
            orientation='h',
            color="Hourly Impact",
            labels={"Hourly Impact": "Adjusted Hourly Yield ($/hr)"},
            color_continuous_scale='IceFire',
            template="plotly_dark"
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_status:
        st.subheader("Urgency Monitoring")
        critical_threshold = 14
        urgent_leads = df[df['Days Remaining'] <= critical_threshold]

        if not urgent_leads.empty:
            priority_target = urgent_leads.loc[urgent_leads['Hourly Impact'].idxmax()]
            st.warning(f"**CRITICAL ACTION REQUIRED**")
            st.write(f"Target: {priority_target['Identification']}")
            st.write(f"Deadline: {priority_target['Days Remaining']} Days")
            st.write(f"Adjusted Yield: ${priority_target['Hourly Impact']}/hr")
        else:
            st.success("Temporal parameters stable. No immediate deadlines detected.")

     st.subheader("Asset Allocation Matrix")
     df_final = df.sort_values(by="Hourly Impact", ascending=False)
     st.dataframe(df_final, use_container_width=True, hide_index=True)

     csv_data = df_final.to_csv(index=False).encode('utf-8')
     st.download_button(
         label="Download Comprehensive Strategy Report (CSV)",
         data=csv_data,
         file_name=f"ScholarQuant_Strategy_{date.today().csv",
         mime='text/csv',
     }
     
st.write("---")
st.caption("ScholarQuant v1.0 | Data-Driven Academic Strategy | Developed in Calgary, AB")
