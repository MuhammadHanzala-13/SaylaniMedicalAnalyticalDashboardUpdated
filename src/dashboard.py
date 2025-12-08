import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaning import main as clean_data_main
from src.json_kb_generator import JSONKnowledgeBaseGenerator

# Page config with custom theme
st.set_page_config(
    page_title="Saylani Health Desk Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=""
)

# Custom CSS for high-contrast professional theme
st.markdown("""
<style>
    /* ... (CSS styles kept as is) ... */
    /* Main background - Very Dark Navy */
    .main {
        background-color: #0A1929;
    }
    
    /* Metric cards - Dark Slate Blue containers */
    .stMetric {
        background-color: #14344F !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        border: 1px solid rgba(79, 159, 253, 0.2) !important;
    }
    
    /* Metric labels - Very Light Blue-Grey */
    .stMetric label {
        color: #E0E7FF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metric values - Very Light Blue-Grey */
    .stMetric [data-testid="stMetricValue"] {
        color: #E0E7FF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    /* Metric delta - Vibrant Azure */
    .stMetric [data-testid="stMetricDelta"] {
        color: #4F9FFD !important;
    }
    
    /* Headers - Very Light Blue-Grey */
    h1 {
        color: #E0E7FF !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    h2, h3 {
        color: #E0E7FF !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar - Dark Slate Blue */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #14344F !important;
        border-right: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    .css-1d391kg p, [data-testid="stSidebar"] p {
        color: #E0E7FF !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #E0E7FF !important;
    }
    
    /* Context and answer boxes */
    .context-box {
        background-color: #14344F !important;
        padding: 15px !important;
        border-radius: 8px !important;
        border-left: 4px solid #4F9FFD !important;
        margin: 10px 0 !important;
        color: #E0E7FF !important;
    }
    
    .answer-box {
        background-color: #14344F !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border-left: 4px solid #4F9FFD !important;
        margin: 15px 0 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #E0E7FF !important;
    }
    
    .answer-box h4 {
        color: #4F9FFD !important;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #14344F !important;
        color: #E0E7FF !important;
        border: 2px solid #4F9FFD !important;
    }
    
    .stTextInput input::placeholder {
        color: #9AA5B1 !important;
    }
    
    /* Buttons - Vibrant Azure */
    .stButton button {
        background-color: #4F9FFD !important;
        color: #0A1929 !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #6BB0FF !important;
        box-shadow: 0 4px 12px rgba(79, 159, 253, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #14344F !important;
        color: #E0E7FF !important;
        font-weight: 600 !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #E0E7FF !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: #14344F !important;
        border-color: #4F9FFD !important;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 10px !important;
        background-color: #14344F !important;
        color: #E0E7FF !important;
        border: 1px solid rgba(79, 159, 253, 0.3);
    }
    
    /* Plotly charts background - Dark Slate Blue */
    .js-plotly-plot {
        background-color: #14344F !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    /* Plotly chart paper background */
    .plot-container {
        background-color: #14344F !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(79, 159, 253, 0.2) !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #E0E7FF !important;
    }
    
    /* Code blocks */
    code {
        background-color: #14344F !important;
        color: #4F9FFD !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Title with high-contrast theme
st.markdown("""
<h1 style='text-align: center; color: #E0E7FF; font-size: 3em; font-weight: 700; margin-bottom: 30px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>
Saylani Medical Help Desk Analytics
</h1>
""", unsafe_allow_html=True)

# Load Data first (before sidebar filters)
@st.cache_data
def load_data():
    csv_path = "data/cleaned/appointments.csv"
    kb_path = "data/knowledge_base/analytics_kb.json"
    
    # 1. Check and generate CSVs if missing
    if not os.path.exists(csv_path):
        with st.spinner("Data not found. Generating data from raw files..."):
            try:
                os.makedirs("data/cleaned", exist_ok=True)
                clean_data_main()
                st.success("Data generated successfully!")
            except Exception as e:
                st.error(f"Failed to generate data: {str(e)}")
                return None

    # 2. Check and generate Knowledge Base (JSON) if missing
    if not os.path.exists(kb_path):
        with st.spinner("Building AI Knowledge Base..."):
            try:
                kb_gen = JSONKnowledgeBaseGenerator()
                
                # Load necessary DFs for KB generation
                doctors = pd.read_csv("data/cleaned/doctors.csv")
                branches = pd.read_csv("data/cleaned/branches.csv")
                diseases = pd.read_csv("data/cleaned/diseases.csv")
                appointments = pd.read_csv("data/cleaned/appointments.csv")
                
                kb_gen.generate_from_data(doctors, branches, diseases, appointments)
                st.success("Knowledge Base built successfully!")
            except Exception as e:
                st.warning(f"Could not build Knowledge Base: {e}")
                # Don't stop execution, just warn

    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

df = load_data()

# Sidebar with enhanced styling
st.sidebar.markdown("### Control Panel")
if st.sidebar.button("Rebuild Knowledge Base"):
    try:
        os.remove("data/knowledge_base/analytics_kb.json")
        st.cache_data.clear()
        st.rerun()
    except:
        pass
st.sidebar.markdown("---")

# Get unique branch names dynamically from data
if df is not None and 'branch_name' in df.columns:
    branch_options = ["All"] + sorted(df['branch_name'].unique().tolist())
else:
    branch_options = ["All"]

branch_filter = st.sidebar.selectbox(
    "Select Branch",
    branch_options,
    help="Filter data by specific branch"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")

if df is not None and len(df) > 0:
    # Sidebar quick stats
    st.sidebar.metric("Total Records", len(df))
    st.sidebar.metric("Branches", df['branch_name'].nunique() if 'branch_name' in df.columns else 0)
    
    if branch_filter != "All":
        df = df[df['branch_name'] == branch_filter]
    
    if len(df) == 0:
        st.warning(f"No data available for branch {branch_filter}. Please select a different branch.")
    else:
        # Summary Metrics with enhanced styling
        st.markdown("### Key Performance Indicators")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "Total Patients",
                f"{len(df):,}",
                delta=None,
                help="Total number of patient visits"
            )
        
        with metric_col2:
            unique_doctors = df['doctor_name'].nunique() if 'doctor_name' in df.columns else 0
            st.metric(
                "Active Doctors",
                unique_doctors,
                help="Number of doctors serving patients"
            )
        
        with metric_col3:
            unique_diseases = df['disease_name'].nunique() if 'disease_name' in df.columns else 0
            st.metric(
                "Disease Types",
                unique_diseases,
                help="Unique diseases being treated"
            )
        
        with metric_col4:
            unique_areas = df['area'].nunique() if 'area' in df.columns else 0
            st.metric(
                "Areas Served",
                unique_areas,
                help="Geographic coverage"
            )
        
        st.markdown("---")
        
        # Create tabs for better organization
        tab1, tab2, tab3, tab4 = st.tabs(["Overview & Trends", "Disease Analytics", "Doctor & Branch", "Advanced Correlations"])
        
        # --- TAB 1: OVERVIEW & TRENDS ---
        with tab1:
            st.markdown("### Temporal & Demographics Analysis")
            
            # Row 1: Time Series
            if 'visit_timestamp' in df.columns and len(df) > 0:
                df_copy = df.copy()
                df_copy['visit_timestamp'] = pd.to_datetime(df_copy['visit_timestamp'], errors='coerce')
                df_copy = df_copy.dropna(subset=['visit_timestamp'])
                
                if len(df_copy) > 0:
                    daily_counts = df_copy.set_index('visit_timestamp').resample('D').size().reset_index()
                    daily_counts.columns = ['Date', 'Visits']
                    
                    fig_trend = px.line(
                        daily_counts, x='Date', y='Visits', markers=True,
                        title="Daily Patient Visits Trend",
                        color_discrete_sequence=['#4F9FFD']
                    )
                    fig_trend.update_layout(
                        height=400, plot_bgcolor='#14344F', paper_bgcolor='#14344F',
                        font=dict(color='#E0E7FF'),
                        xaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)'),
                        yaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)')
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
            
            # Row 2: Pie Charts (Gender & Branch)
            col_p1, col_p2 = st.columns(2)
            
            with col_p1:
                if 'gender' in df.columns:
                    gender_counts = df['gender'].value_counts()
                    fig_gender = px.pie(
                        values=gender_counts.values, names=gender_counts.index,
                        title="Patient Gender Distribution",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        hole=0.4
                    )
                    fig_gender.update_layout(paper_bgcolor='#14344F', font=dict(color='#E0E7FF'))
                    st.plotly_chart(fig_gender, use_container_width=True)
            
            with col_p2:
                if 'branch_name' in df.columns:
                    branch_counts = df['branch_name'].value_counts()
                    fig_branch = px.pie(
                        values=branch_counts.values, names=branch_counts.index,
                        title="Patient Distribution by Branch",
                        color_discrete_sequence=px.colors.qualitative.Safe,
                        hole=0.4
                    )
                    fig_branch.update_layout(paper_bgcolor='#14344F', font=dict(color='#E0E7FF'))
                    st.plotly_chart(fig_branch, use_container_width=True)

        # --- TAB 2: DISEASE ANALYTICS ---
        with tab2:
            st.markdown("### Disease Prevalence & Pareto Analysis")
            
            if 'disease_name' in df.columns:
                disease_counts = df['disease_name'].value_counts().reset_index()
                disease_counts.columns = ['Disease', 'Count']
                
                # Calculate Cumulative Percentage
                disease_counts['Cumulative Percentage'] = (disease_counts['Count'].cumsum() / disease_counts['Count'].sum()) * 100
                
                # Pareto Chart (Bar + Line)
                fig_pareto = go.Figure()
                
                # Bar Chart (Counts)
                fig_pareto.add_trace(go.Bar(
                    x=disease_counts['Disease'].head(20),
                    y=disease_counts['Count'].head(20),
                    name='Cases',
                    marker_color='#4F9FFD'
                ))
                
                # Line Chart (Cumulative %)
                fig_pareto.add_trace(go.Scatter(
                    x=disease_counts['Disease'].head(20),
                    y=disease_counts['Cumulative Percentage'].head(20),
                    name='Cumulative %',
                    yaxis='y2',
                    mode='lines+markers',
                    marker=dict(color='#FF6B6B'),
                    line=dict(width=3)
                ))
                
                fig_pareto.update_layout(
                    title="Disease Pareto Chart (Top 20)",
                    yaxis=dict(title="Number of Cases", gridcolor='rgba(224, 231, 255, 0.1)'),
                    yaxis2=dict(title="Cumulative Percentage", overlaying='y', side='right', range=[0, 110], showgrid=False),
                    plot_bgcolor='#14344F', paper_bgcolor='#14344F',
                    font=dict(color='#E0E7FF'),
                    legend=dict(x=0.8, y=1.1, orientation='h'),
                    height=500
                )
                st.plotly_chart(fig_pareto, use_container_width=True)
                
                # Treemap with enhanced visuals
                st.markdown("### Disease Hierarchy (Treemap)")
                fig_tree = px.treemap(
                    disease_counts, 
                    path=['Disease'], 
                    values='Count',
                    color='Count', 
                    color_continuous_scale='Spectral',
                    title="Disease Volume Treemap",
                    hover_data={'Count': True, 'Cumulative Percentage': True}
                )
                fig_tree.update_traces(
                    textinfo="label+value+percent entry",
                    marker=dict(line=dict(width=2, color='#14344F')),
                    textfont=dict(size=14)
                )
                fig_tree.update_layout(
                    height=650,
                    paper_bgcolor='#14344F',
                    font=dict(color='#E0E7FF', size=14),
                    margin=dict(t=50, l=10, r=10, b=10)
                )
                st.plotly_chart(fig_tree, use_container_width=True)

        # --- TAB 3: DOCTOR & BRANCH ---
        with tab3:
            st.markdown("### Staff Performance & Geographic Reach")
            
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                if 'doctor_name' in df.columns:
                    top_doctors = df['doctor_name'].value_counts().head(10)
                    fig_doc = px.bar(
                        x=top_doctors.values, y=top_doctors.index, orientation='h',
                        title="Top 10 Busiest Doctors",
                        labels={'x': 'Patients', 'y': 'Doctor'},
                        color=top_doctors.values, color_continuous_scale='Plasma'
                    )
                    fig_doc.update_layout(plot_bgcolor='#14344F', paper_bgcolor='#14344F', font=dict(color='#E0E7FF'))
                    st.plotly_chart(fig_doc, use_container_width=True)
            
            with col_d2:
                if 'area' in df.columns:
                    top_areas = df['area'].value_counts().head(10)
                    fig_area = px.bar(
                        x=top_areas.index, y=top_areas.values,
                        title="Top 10 Patient Areas",
                        labels={'x': 'Area', 'y': 'Patients'},
                        color=top_areas.values, color_continuous_scale='Turbo'
                    )
                    fig_area.update_layout(plot_bgcolor='#14344F', paper_bgcolor='#14344F', font=dict(color='#E0E7FF'))
                    st.plotly_chart(fig_area, use_container_width=True)

        # --- TAB 4: ADVANCED CORRELATIONS ---
        with tab4:
            st.markdown("### Variable Relationships (Heatmaps)")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                x_axis = st.selectbox("Select X-Axis Variable", ['branch_name', 'gender', 'area', 'specialty'], index=0)
            with col_c2:
                y_axis = st.selectbox("Select Y-Axis Variable", ['disease_name', 'doctor_name', 'gender'], index=0)
            
            if x_axis in df.columns and y_axis in df.columns:
                # Create Cross-tabulation
                crosstab = pd.crosstab(df[y_axis], df[x_axis])
                
                # Enhanced Heatmap with text values and better sizing
                fig_corr = px.imshow(
                    crosstab,
                    labels=dict(x=x_axis, y=y_axis, color="Count"),
                    x=crosstab.columns,
                    y=crosstab.index,
                    color_continuous_scale='Viridis',
                    title=f"Heatmap: {y_axis} vs {x_axis}",
                    text_auto=True,
                    aspect="auto"
                )
                fig_corr.update_layout(
                    height=800,
                    plot_bgcolor='#14344F', 
                    paper_bgcolor='#14344F',
                    font=dict(color='#E0E7FF', size=12),
                    xaxis=dict(tickangle=-45, side='bottom', title_font=dict(size=14)),
                    yaxis=dict(side='left', title_font=dict(size=14)),
                    margin=dict(t=60, l=50, r=50, b=100)
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("Selected variables not found in dataset.")
    
    # AI Assistant Section with enhanced UI
    st.markdown("---")
    st.markdown("### AI Medical Assistant")
    st.markdown("Ask questions about doctors, diseases, schedules, and more!")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Your Question:",
            placeholder="e.g., Explain the disease trends graph, Who is the busiest doctor?, What are the top diseases?",
            help="Ask about doctors, diseases, or ask for an explanation of the analytics graphs shown above."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        ask_button = st.button("Ask AI", type="primary", use_container_width=True)
    
    if ask_button and query:
        with st.spinner("Thinking..."):
            try:
                # Initialize LLM and KB directly (Lazy initialization to save resources)
                from src.llm import LLMGenerator
                from src.json_kb import JSONKnowledgeBase
                
                llm_gen = LLMGenerator()
                kb = JSONKnowledgeBase()

                # Get full context from KB
                context_text = kb.get_full_context()
                
                # Generate answer using LLM Generator directly
                # This handles API calls and fallbacks internally
                answer = llm_gen.generate_answer(query, context_text)
                
                # Determine source for display
                source_type = "Gemini API" if llm_gen.api_available and "Extracted from Analytics Knowledge Base" not in answer else "JSON Knowledge Base (Fallback)"
                
                # Display answer in a styled box
                st.markdown(f"""
                <div class="answer-box">
                    <h4 style="color: #059669; margin-top: 0;">Answer:</h4>
                    <p style="margin-bottom: 0;">{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show source info
                if source_type == "Gemini API":
                    st.success(f"Generated by AI ({source_type})")
                else:
                    st.info(f"Source: {source_type}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif ask_button:
        st.warning("Please enter a question first!")

else:
    st.error("Data not found!")
    # Allow manual trigger of cleaning if something goes wrong
    if st.button("Run Data Pipeline Manually"):
        with st.spinner("Running pipeline..."):
            try:
                clean_data_main()
                st.success("Pipeline finished! Please refresh the page.")
                st.rerun()
            except Exception as e:
                st.error(f"Pipeline failed: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9AA5B1; padding: 20px;'>
    <p><strong style='color: #E0E7FF;'>Saylani Medical Help Desk System v1.2</strong></p>
    <p>Developed by <strong>Muhammad Hanzala</strong> from Saylani Health Management Team-AI || Powered by FastAPI & Streamlit.</p>
</div>
""", unsafe_allow_html=True)
