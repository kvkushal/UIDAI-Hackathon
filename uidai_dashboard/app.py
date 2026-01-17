"""
Aadhaar N.E.X.U.S - National Equity eXecution & Utilization System
A data-driven planning and early-warning system that measures digital equity,
anticipates Aadhaar demand, and simulates where UIDAI should act first.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Aadhaar N.E.X.U.S - National Equity System",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# METRIC DEFINITIONS & TOOLTIPS
# =============================================================================
METRIC_INFO = {
    'DEI': {
        'name': 'Digital Equity Index',
        'short': 'DEI',
        'tooltip': 'Overall score measuring digital service equity. Combines access, responsiveness, inclusion, stability, and visibility. Higher is better.',
        'higher_is_better': True
    },
    'ASS': {
        'name': 'Access Health Score',
        'short': 'Access',
        'tooltip': 'Measures how easily citizens can access Aadhaar services. Low scores indicate strained infrastructure. Higher is better.',
        'higher_is_better': True
    },
    'UBS': {
        'name': 'Update Load Score',
        'short': 'Update Load',
        'tooltip': 'Measures burden of update requests on the system. High scores indicate heavy biometric update activity. Lower is better.',
        'higher_is_better': False
    },
    'SRS': {
        'name': 'Stability Score',
        'short': 'Stability',
        'tooltip': 'Measures consistency of service delivery. High scores indicate unpredictable activity or downtime. Lower is better.',
        'higher_is_better': False
    }
}

# District-specific detailed suggestions for txt report (3-4 lines)
DETAILED_SUGGESTIONS = {
    'access_stress': '''The district shows signs of enrollment infrastructure strain. Consider the following actions:
1. Increase the number of active enrollment centers, particularly in rural areas
2. Deploy mobile enrollment vans to reach underserved populations
3. Partner with local government offices (panchayats, schools) for additional enrollment points
4. Review and optimize appointment scheduling to reduce wait times''',
    
    'update_burden': '''The district is experiencing high update request volumes. Recommended interventions:
1. Set up dedicated biometric update camps in high-demand areas
2. Implement online appointment booking to manage walk-in crowds
3. Consider extending operating hours during peak update periods
4. Ensure adequate staff and equipment to handle update volumes efficiently''',
    
    'stability_risk': '''Service delivery in this district shows inconsistency. Key improvements needed:
1. Audit system uptime and address recurring technical failures
2. Ensure reliable power backup and internet connectivity at all centers
3. Train staff on troubleshooting common issues to minimize downtime
4. Establish regular maintenance schedules for all enrollment devices''',
    
    'critical': '''This district requires immediate, comprehensive intervention:
1. Conduct a full assessment of current infrastructure and staffing
2. Allocate emergency resources to address critical gaps
3. Establish a dedicated task force to monitor daily operations
4. Implement weekly progress tracking with escalation protocols''',
    
    'healthy': '''The district is performing well. To maintain and improve:
1. Continue regular monitoring of all key metrics
2. Document best practices for knowledge sharing with other districts
3. Consider pilot programs for new service innovations
4. Maintain staff training and equipment maintenance schedules'''
}

# Simple one-line suggestions for dashboard display
SIMPLE_SUGGESTIONS = {
    'access_stress': '📌 Add more enrollment centers and deploy mobile vans',
    'update_burden': '🔄 Set up dedicated update camps',
    'stability_risk': '⚡ Audit system uptime and power/internet',
    'critical': '🚨 Allocate emergency resources now',
    'healthy': '✅ Maintain current operations'
}

def get_badge(score, metric_key):
    """Return badge text and color based on score and metric type."""
    higher_is_better = METRIC_INFO[metric_key]['higher_is_better']
    
    if higher_is_better:
        if score >= 0.75:
            return "Excellent", "#22c55e", "🟢"
        elif score >= 0.5:
            return "Good", "#84cc16", "🟡"
        elif score >= 0.3:
            return "Needs Attention", "#f59e0b", "🟠"
        else:
            return "Critical", "#ef4444", "🔴"
    else:
        if score <= 0.25:
            return "Excellent", "#22c55e", "🟢"
        elif score <= 0.5:
            return "Good", "#84cc16", "🟡"
        elif score <= 0.7:
            return "Needs Attention", "#f59e0b", "🟠"
        else:
            return "Critical", "#ef4444", "🔴"

def get_issue_type(row):
    """Determine the primary issue type for a district."""
    if row['DEI'] < 0.5:
        return 'critical'
    elif row['ASS'] < 0.5:
        return 'access_stress'
    elif row['UBS'] > 0.7:
        return 'update_burden'
    elif row['SRS'] > 0.6:
        return 'stability_risk'
    else:
        return 'healthy'

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    """Load the consolidated district equity data."""
    # Use absolute path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'district_equity_all_india.csv')
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Fallback for local testing or different CWD
        st.error(f"Data file not found at: {file_path}")
        st.stop()
        
    return df

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_score_color(score, reverse=False):
    """Return color based on score value."""
    if reverse:
        if score > 0.7:
            return "#ef4444"
        elif score > 0.5:
            return "#eab308"
        else:
            return "#22c55e"
    else:
        if score >= 0.7:
            return "#22c55e"
        elif score >= 0.5:
            return "#eab308"
        else:
            return "#ef4444"

def get_risk_category(row):
    """Classify district into risk categories."""
    if row['ASS'] < 0.5:
        return "Access Stress"
    elif row['UBS'] > 0.7:
        return "Update Burden"
    elif row['SRS'] > 0.6:
        return "Stability Risk"
    else:
        return "Healthy"

def get_recommendation(row):
    """Generate action recommendation based on scores."""
    if row['DEI'] < 0.5:
        return {
            'level': 'critical',
            'title': 'Critical Equity Gap',
            'message': 'This district requires immediate attention. DEI score is critically low.',
            'action': 'Prioritize comprehensive resource allocation and infrastructure development.'
        }
    
    if row['ASS'] < 0.5:
        return {
            'level': 'warning',
            'title': 'High Access Stress',
            'message': 'District faces challenges in Aadhaar enrollment accessibility.',
            'action': 'Focus on enrollment infrastructure - add more centers, improve connectivity.'
        }
    
    if row['UBS'] > 0.7:
        return {
            'level': 'warning',
            'title': 'Update Overload',
            'message': 'High volume of update requests straining system capacity.',
            'action': 'Streamline update processes - consider mobile camps, optimize workflows.'
        }
    
    if row['SRS'] > 0.6:
        return {
            'level': 'warning',
            'title': 'Stability Concerns',
            'message': 'Inconsistent service delivery detected.',
            'action': 'Review system uptime, data quality, and operational consistency.'
        }
    
    return {
        'level': 'good',
        'title': 'District Performing Well',
        'message': 'All metrics are within acceptable ranges.',
        'action': 'Maintain current operations and continue monitoring.'
    }

def get_state_suggestions(state_df):
    """Generate state-level suggestions based on aggregate metrics."""
    suggestions = []
    
    avg_dei = state_df['DEI'].mean()
    
    # Count districts with issues
    low_dei = len(state_df[state_df['DEI'] < 0.5])
    access_stress = len(state_df[state_df['ASS'] < 0.5])
    update_burden = len(state_df[state_df['UBS'] > 0.7])
    stability_risk = len(state_df[state_df['SRS'] > 0.6])
    
    if low_dei > 0:
        suggestions.append(f"🚨 **{low_dei} district(s)** have critically low DEI scores and need immediate attention")
    
    if access_stress > 0:
        suggestions.append(f"📍 **{access_stress} district(s)** face access stress - consider expanding enrollment infrastructure")
    
    if update_burden > 0:
        suggestions.append(f"🔄 **{update_burden} district(s)** have high update burden - deploy dedicated update camps")
    
    if stability_risk > 0:
        suggestions.append(f"⚡ **{stability_risk} district(s)** show stability risks - audit system uptime and connectivity")
    
    if avg_dei >= 0.7:
        suggestions.append("✅ Overall state performance is **excellent** - focus on maintaining standards")
    elif avg_dei >= 0.5:
        suggestions.append("📊 Overall state performance is **moderate** - targeted improvements can yield significant gains")
    else:
        suggestions.append("⚠️ State-wide performance is **below par** - comprehensive intervention strategy needed")
    
    # Best and worst performers
    best = state_df.loc[state_df['DEI'].idxmax()]
    worst = state_df.loc[state_df['DEI'].idxmin()]
    suggestions.append(f"🏆 Best performer: **{best['district'].title()}** (DEI: {best['DEI']:.3f})")
    suggestions.append(f"📉 Needs most attention: **{worst['district'].title()}** (DEI: {worst['DEI']:.3f})")
    
    return suggestions

def generate_district_report(state, district, data, state_data):
    """Generate a detailed text report for a district."""
    issue_type = get_issue_type(data)
    detailed_suggestion = DETAILED_SUGGESTIONS.get(issue_type, DETAILED_SUGGESTIONS['healthy'])
    rec = get_recommendation(data)
    
    report = f"""
================================================================================
                    AADHAAR N.E.X.U.S - DISTRICT REPORT
================================================================================

STATE: {state}
DISTRICT: {district.title()}
REPORT DATE: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

--------------------------------------------------------------------------------
                              PERFORMANCE SCORES
--------------------------------------------------------------------------------

  METRIC                    SCORE      STATE AVG    DIFFERENCE    STATUS
  -------------------------------------------------------------------------
  Digital Equity Index      {data['DEI']:.3f}      {state_data['DEI'].mean():.3f}        {data['DEI'] - state_data['DEI'].mean():+.3f}        {get_badge(data['DEI'], 'DEI')[0]}
  Access Health Score       {data['ASS']:.3f}      {state_data['ASS'].mean():.3f}        {data['ASS'] - state_data['ASS'].mean():+.3f}        {get_badge(data['ASS'], 'ASS')[0]}
  Update Load Score         {data['UBS']:.3f}      {state_data['UBS'].mean():.3f}        {data['UBS'] - state_data['UBS'].mean():+.3f}        {get_badge(data['UBS'], 'UBS')[0]}
  Stability Score           {data['SRS']:.3f}      {state_data['SRS'].mean():.3f}        {data['SRS'] - state_data['SRS'].mean():+.3f}        {get_badge(data['SRS'], 'SRS')[0]}

--------------------------------------------------------------------------------
                               ASSESSMENT
--------------------------------------------------------------------------------

STATUS: {rec['title']}

SUMMARY:
{rec['message']}

--------------------------------------------------------------------------------
                        DETAILED RECOMMENDATIONS
--------------------------------------------------------------------------------

{detailed_suggestion}

--------------------------------------------------------------------------------
                            METRIC DEFINITIONS
--------------------------------------------------------------------------------

* DEI (Digital Equity Index): Overall composite score measuring balanced 
  access, responsiveness, inclusion, stability, and visibility. Range: 0-1.
  Higher scores indicate better digital equity.

* Access Health Score: Measures enrollment accessibility and infrastructure 
  utilization. Lower scores suggest strained or underutilized centers.

* Update Load Score: Tracks biometric and demographic update volumes.
  Higher scores indicate heavy update burden on the system.

* Stability Score: Measures operational consistency and service reliability.
  Higher scores indicate unpredictable or inconsistent service delivery.

================================================================================
                              END OF REPORT
================================================================================
"""
    return report

# Function to style the dataframe
def highlight_score(val, metric):
    if metric in ['DEI', 'Access']:
        if val >= 0.7: return 'background-color: #dcfce7; color: #14532d' # Green
        if val >= 0.4: return 'background-color: #fef9c3; color: #713f12' # Yellow
        return 'background-color: #fee2e2; color: #7f1d1d' # Red
    else: # Update Load, Stability (Lower is better)
        if val <= 0.4: return 'background-color: #dcfce7; color: #14532d' # Green
        if val <= 0.7: return 'background-color: #fef9c3; color: #713f12' # Yellow
        return 'background-color: #fee2e2; color: #7f1d1d' # Red

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    # Load data
    df = load_data()
    
    # =========================================================================
    # HEADER
    # =========================================================================
    st.title("Aadhaar N.E.X.U.S")
    st.caption("**National Equity eXecution & Utilization System** | A data-driven planning and early-warning system")
    
    st.divider()
    
    # ==========================================================================
    # SIDEBAR
    # ==========================================================================
    with st.sidebar:
        st.header("Region Selection")
        
        # State selection
        states = sorted(df['state'].unique())
        selected_state = st.selectbox(
            "Select State/UT",
            states,
            index=0
        )
        
        # Filter data for selected state
        state_df = df[df['state'] == selected_state].copy()
        state_df['risk_category'] = state_df.apply(get_risk_category, axis=1)
        
        st.divider()
        
        # State overview
        st.subheader("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Districts", len(state_df))
        with col2:
            st.metric("Avg DEI", f"{state_df['DEI'].mean():.3f}")
        
        # Risk breakdown
        risk_counts = state_df['risk_category'].value_counts()
        
        st.subheader("Risk Summary")
        for category in ['Healthy', 'Access Stress', 'Update Burden', 'Stability Risk']:
            count = risk_counts.get(category, 0)
            if category == 'Healthy':
                st.success(f"[OK] {category}: {count}")
            elif count > 0:
                st.warning(f"[!] {category}: {count}")
            else:
                st.info(f"[ ] {category}: {count}")
        
        st.divider()
        
        # GLOSSARY SECTION
        st.subheader("Metric Glossary")
        
        with st.expander("What do these metrics mean?"):
            for key, info in METRIC_INFO.items():
                direction = "[Higher is better]" if info['higher_is_better'] else "[Lower is better]"
                st.markdown(f"**{info['name']}**")
                st.caption(f"{info['tooltip']}")
                st.caption(f"*{direction}*")
                st.markdown("")
    
    # ==========================================================================
    # MAIN CONTENT - STATE LEVEL SUMMARY
    # ==========================================================================
    
    st.header("State Performance Summary")
    st.caption("Hover over metric names to see explanations")
    
    avg_dei = state_df['DEI'].mean()
    avg_ass = state_df['ASS'].mean()
    avg_ubs = state_df['UBS'].mean()
    avg_srs = state_df['SRS'].mean()
    
    # KPI Cards using native Streamlit
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        badge_text, _, badge_icon = get_badge(avg_dei, 'DEI')
        st.metric(
            label="Digital Equity Index",
            value=f"{avg_dei:.3f}",
            delta=f"{badge_icon} {badge_text}",
            help=METRIC_INFO['DEI']['tooltip']
        )
    
    with col2:
        badge_text, _, badge_icon = get_badge(avg_ass, 'ASS')
        st.metric(
            label="Access Health Score",
            value=f"{avg_ass:.3f}",
            delta=f"{badge_icon} {badge_text}",
            help=METRIC_INFO['ASS']['tooltip']
        )
    
    with col3:
        badge_text, _, badge_icon = get_badge(avg_ubs, 'UBS')
        st.metric(
            label="Update Load Score",
            value=f"{avg_ubs:.3f}",
            delta=f"{badge_icon} {badge_text}",
            delta_color="inverse",
            help=METRIC_INFO['UBS']['tooltip']
        )
    
    with col4:
        badge_text, _, badge_icon = get_badge(avg_srs, 'SRS')
        st.metric(
            label="Stability Score",
            value=f"{avg_srs:.3f}",
            delta=f"{badge_icon} {badge_text}",
            delta_color="inverse",
            help=METRIC_INFO['SRS']['tooltip']
        )
    
    # ==========================================================================
    # STATE-LEVEL SUGGESTIONS
    # ==========================================================================
    st.divider()
    st.subheader("State-Level Insights & Recommendations")
    
    state_suggestions = get_state_suggestions(state_df)
    for suggestion in state_suggestions:
        st.markdown(suggestion)
    
    # ==========================================================================
    # VISUALIZATIONS
    # ==========================================================================
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("District DEI Ranking")
        chart_df = state_df.sort_values('DEI', ascending=True)
        colors = [get_score_color(dei) for dei in chart_df['DEI']]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=chart_df['district'].str.title(),
            x=chart_df['DEI'],
            orientation='h',
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>DEI: %{x:.3f}<extra></extra>",
            text=[f"{dei:.2f}" for dei in chart_df['DEI']],
            textposition='outside'
        ))
        
        fig_bar.update_layout(
            height=max(400, len(state_df) * 25),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Digital Equity Index (DEI)",
            yaxis_title="",
            showlegend=False,
            xaxis=dict(range=[0, 1])
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_chart2:
        st.subheader("Risk Composition")
        
        risk_data = state_df['risk_category'].value_counts().reset_index()
        risk_data.columns = ['Category', 'Count']
        
        color_map = {
            'Healthy': '#22c55e',
            'Access Stress': '#f59e0b',
            'Update Burden': '#ef4444',
            'Stability Risk': '#8b5cf6'
        }
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=risk_data['Category'],
            values=risk_data['Count'],
            hole=0.5,
            marker_colors=[color_map.get(cat, '#94a3b8') for cat in risk_data['Category']],
            textinfo='label+value',
            textposition='outside'
        )])
        
        fig_donut.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=40),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
        
        st.plotly_chart(fig_donut, use_container_width=True)

    # ==========================================================================
    # DISTRICT RANKING TABLE (HEATMAP STYLE)
    # ==========================================================================
    st.divider()
    st.subheader("District Scores Table")

    table_data = state_df[['district', 'DEI', 'ASS', 'UBS', 'SRS', 'risk_category']].copy()
    table_data.columns = ['District', 'DEI', 'Access', 'Update Load', 'Stability', 'Status']
    table_data['District'] = table_data['District'].str.title()
    
    # Sort by DEI descending
    table_data = table_data.sort_values('DEI', ascending=False)
    
    # Apply styling
    styled_table = table_data.style.map(lambda x: highlight_score(x, 'DEI'), subset=['DEI'])\
                                   .map(lambda x: highlight_score(x, 'Access'), subset=['Access'])\
                                   .map(lambda x: highlight_score(x, 'UBS'), subset=['Update Load'])\
                                   .map(lambda x: highlight_score(x, 'SRS'), subset=['Stability'])\
                                   .format("{:.3f}", subset=['DEI', 'Access', 'Update Load', 'Stability'])
    
    st.dataframe(
        styled_table,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # ==========================================================================
    # DISTRICT DETAIL VIEW
    # ==========================================================================
    st.divider()
    st.header("District Detail View")
    
    # Use vertical_alignment="bottom" to align Dropdown and Button
    col_select, col_export = st.columns([3, 1], vertical_alignment="bottom")
    
    with col_select:
        districts = sorted(state_df['district'].str.title().unique())
        selected_district_detail = st.selectbox(
            "Select District for Details",
            districts,
            index=0,
            key="detail_district_selector"
        )
    
    # Get district data
    district_data = state_df[state_df['district'].str.title() == selected_district_detail].iloc[0]
    recommendation = get_recommendation(district_data)
    issue_type = get_issue_type(district_data)
    
    # Export button
    with col_export:
        report_text = generate_district_report(
            selected_state, 
            selected_district_detail, 
            district_data, 
            state_df
        )
        st.download_button(
            label="Download Report",
            data=report_text,
            file_name=f"{selected_district_detail.lower().replace(' ', '_')}_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # District Score Cards - using native Streamlit metrics
    st.subheader("Score Breakdown")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        badge_text, _, badge_icon = get_badge(district_data['DEI'], 'DEI')
        delta_val = district_data['DEI'] - avg_dei
        st.metric(
            label="Digital Equity Index",
            value=f"{district_data['DEI']:.3f}",
            delta=f"{delta_val:+.3f} vs state",
            help=METRIC_INFO['DEI']['tooltip']
        )
        st.caption(f"{badge_icon} {badge_text}")
    
    with col2:
        badge_text, _, badge_icon = get_badge(district_data['ASS'], 'ASS')
        delta_val = district_data['ASS'] - avg_ass
        st.metric(
            label="Access Health Score",
            value=f"{district_data['ASS']:.3f}",
            delta=f"{delta_val:+.3f} vs state",
            help=METRIC_INFO['ASS']['tooltip']
        )
        st.caption(f"{badge_icon} {badge_text}")
    
    with col3:
        badge_text, _, badge_icon = get_badge(district_data['UBS'], 'UBS')
        delta_val = district_data['UBS'] - avg_ubs
        st.metric(
            label="Update Load Score",
            value=f"{district_data['UBS']:.3f}",
            delta=f"{delta_val:+.3f} vs state",
            delta_color="inverse",
            help=METRIC_INFO['UBS']['tooltip']
        )
        st.caption(f"{badge_icon} {badge_text}")
    
    with col4:
        badge_text, _, badge_icon = get_badge(district_data['SRS'], 'SRS')
        delta_val = district_data['SRS'] - avg_srs
        st.metric(
            label="Stability Score",
            value=f"{district_data['SRS']:.3f}",
            delta=f"{delta_val:+.3f} vs state",
            delta_color="inverse",
            help=METRIC_INFO['SRS']['tooltip']
        )
        st.caption(f"{badge_icon} {badge_text}")
    
    # Recommendation Panel - using native Streamlit components
    st.subheader("Assessment & Recommendations")
    
    if recommendation['level'] == 'critical':
        st.error(f"[CRITICAL] **{recommendation['title']}**")
    elif recommendation['level'] == 'warning':
        st.warning(f"[WARNING] **{recommendation['title']}**")
    else:
        st.success(f"[OK] **{recommendation['title']}**")
    
    st.info(f"**Assessment:** {recommendation['message']}")
    st.info(f"**Recommended Action:** {recommendation['action']}")
    
    # Simple suggestion on dashboard
    st.markdown("---")
    st.markdown(f"**Quick Improvement:** {SIMPLE_SUGGESTIONS[issue_type]}")
    
    # ==========================================================================
    # RISK SCATTER PLOT
    # ==========================================================================
    st.divider()
    st.header("Risk Analysis Matrix")
    st.caption("Each dot = one district. Size/color = DEI score. Aim for bottom-left (low burden, low risk).")
    
    fig_scatter = px.scatter(
        state_df,
        x='UBS',
        y='SRS',
        color='DEI',
        size='DEI',
        hover_name=state_df['district'].str.title(),
        color_continuous_scale='RdYlGn',
        labels={
            'UBS': 'Update Load Score (lower is better)',
            'SRS': 'Stability Score (lower is better)',
            'DEI': 'Digital Equity Index'
        }
    )
    
    fig_scatter.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig_scatter.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig_scatter.add_annotation(x=0.25, y=0.25, text="[+] Optimal", showarrow=False, font=dict(size=12, color="green"))
    fig_scatter.add_annotation(x=0.75, y=0.75, text="[!] Risk Zone", showarrow=False, font=dict(size=12, color="red"))
    
    fig_scatter.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# =============================================================================
# RUN APP
# =============================================================================
if __name__ == "__main__":
    main()
