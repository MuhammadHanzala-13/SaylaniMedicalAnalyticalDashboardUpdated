import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set beautiful style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Paths
CLEANED_DIR = "data/cleaned"
OUTPUT_DIR = "data/eda_output"

# Beautiful color palettes
COLORS = {
    'primary': ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
    'disease': ['#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3'],
    'doctor': ['#ff9a56', '#ff6a88', '#ffecd2', '#fcb69f'],
    'area': ['#4facfe', '#00f2fe', '#43e97b', '#38f9d7'],
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
}

def create_output_dir():
    """Create output directory for visualizations"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def load_data():
    """Load all cleaned data"""
    print("\n" + "="*70)
    print("LOADING DATA")
    print("="*70)
    
    doctors = pd.read_csv(os.path.join(CLEANED_DIR, "doctors.csv"))
    branches = pd.read_csv(os.path.join(CLEANED_DIR, "branches.csv"))
    diseases = pd.read_csv(os.path.join(CLEANED_DIR, "diseases.csv"))
    appointments = pd.read_csv(os.path.join(CLEANED_DIR, "appointments.csv"))
    
    print(f"Doctors: {len(doctors)} records")
    print(f"Branches: {len(branches)} records")
    print(f"Diseases: {len(diseases)} records")
    print(f"Appointments: {len(appointments)} records")
    
    return doctors, branches, diseases, appointments

def analyze_disease_trends(patients):
    """Analyze and visualize disease trends with beautiful colors"""
    print("\n" + "="*70)
    print("DISEASE TRENDS ANALYSIS")
    print("="*70)
    
    disease_counts = patients['disease_name'].value_counts()
    
    print(f"\nTotal unique diseases: {len(disease_counts)}")
    print(f"\nTop 10 diseases:")
    for disease, count in disease_counts.head(10).items():
        print(f"  - {disease}: {count} cases ({count/len(patients)*100:.1f}%)")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # 1. Horizontal bar chart with gradient
    ax1 = fig.add_subplot(gs[0, :])
    top_10 = disease_counts.head(10)
    colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_10)))
    bars = ax1.barh(range(len(top_10)), top_10.values, color=colors_gradient, edgecolor='white', linewidth=2)
    ax1.set_yticks(range(len(top_10)))
    ax1.set_yticklabels(top_10.index, fontsize=11)
    ax1.set_xlabel('Number of Cases', fontsize=12, fontweight='bold')
    ax1.set_title('Top 10 Most Common Diseases', fontsize=16, fontweight='bold', pad=20)
    ax1.invert_yaxis()
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_10.values)):
        ax1.text(value + 0.5, i, f'{value}', va='center', fontsize=10, fontweight='bold')
    
    # 2. Pie chart with explosion
    ax2 = fig.add_subplot(gs[1, 0])
    top_5 = disease_counts.head(5)
    other = disease_counts[5:].sum()
    pie_data = pd.concat([top_5, pd.Series({'Other': other})])
    
    colors_pie = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#cccccc']
    explode = [0.05] * 5 + [0]
    
    wedges, texts, autotexts = ax2.pie(
        pie_data.values,
        labels=pie_data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors_pie,
        explode=explode,
        shadow=True,
        textprops={'fontsize': 10, 'weight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
    
    ax2.set_title('Disease Distribution (Top 5 + Other)', fontsize=14, fontweight='bold', pad=15)
    
    # 3. Treemap-style visualization
    ax3 = fig.add_subplot(gs[1, 1])
    top_15 = disease_counts.head(15)
    
    # Create a simple treemap effect with bars
    colors_treemap = plt.cm.plasma(np.linspace(0.2, 0.9, len(top_15)))
    bars = ax3.bar(range(len(top_15)), top_15.values, color=colors_treemap, edgecolor='white', linewidth=1.5)
    ax3.set_xticks(range(len(top_15)))
    ax3.set_xticklabels(top_15.index, rotation=45, ha='right', fontsize=9)
    ax3.set_ylabel('Number of Cases', fontsize=11, fontweight='bold')
    ax3.set_title('Top 15 Diseases Comparison', fontsize=14, fontweight='bold', pad=15)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'disease_trends_enhanced.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nSaved: disease_trends_enhanced.png")
    plt.close()

def analyze_doctor_workload(patients, doctors):
    """Analyze doctor workload with stunning visualizations"""
    print("\n" + "="*70)
    print("DOCTOR WORKLOAD ANALYSIS")
    print("="*70)
    
    # Use doctor_name directly from appointments
    workload = patients['doctor_name'].value_counts()
    
    print(f"\nAverage patients per doctor: {workload.mean():.1f}")
    print(f"Max workload: {workload.max()} patients")
    print(f"Min workload: {workload.min()} patients")
    
    print(f"\nTop 10 busiest doctors:")
    for doctor, count in workload.head(10).items():
        print(f"  - {doctor}: {count} patients")
    
    # Create beautiful visualization
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Doctor Workload Analysis Dashboard', fontsize=20, fontweight='bold', y=0.995)
    
    # 1. Top 10 doctors - gradient bars
    ax1 = axes[0, 0]
    top_10 = workload.head(10)
    colors_gradient = plt.cm.coolwarm(np.linspace(0.3, 0.9, len(top_10)))
    bars = ax1.bar(range(len(top_10)), top_10.values, color=colors_gradient, edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(len(top_10)))
    ax1.set_xticklabels(top_10.index, rotation=45, ha='right', fontsize=10)
    ax1.set_ylabel('Number of Patients', fontsize=12, fontweight='bold')
    ax1.set_title('Top 10 Busiest Doctors', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. Distribution histogram with KDE
    ax2 = axes[0, 1]
    ax2.hist(workload, bins=15, color='#667eea', alpha=0.7, edgecolor='black', linewidth=1.5)
    ax2.axvline(workload.mean(), color='#fa709a', linestyle='--', linewidth=3, label=f'Mean: {workload.mean():.1f}')
    ax2.axvline(workload.median(), color='#30cfd0', linestyle='--', linewidth=3, label=f'Median: {workload.median():.1f}')
    ax2.set_xlabel('Number of Patients', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Doctors', fontsize=12, fontweight='bold')
    ax2.set_title('Patient Load Distribution', fontsize=14, fontweight='bold', pad=15)
    ax2.legend(fontsize=11, framealpha=0.9)
    ax2.grid(alpha=0.3, linestyle='--')
    
    # 3. Cumulative distribution
    ax3 = axes[1, 0]
    sorted_workload = workload.sort_values()
    cumulative = np.cumsum(sorted_workload.values)
    cumulative_pct = (cumulative / cumulative[-1]) * 100
    
    ax3.plot(range(len(sorted_workload)), cumulative_pct, color='#764ba2', linewidth=3, marker='o', markersize=4)
    ax3.fill_between(range(len(sorted_workload)), cumulative_pct, alpha=0.3, color='#f093fb')
    ax3.set_xlabel('Doctor Rank (by workload)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Cumulative % of Patients', fontsize=12, fontweight='bold')
    ax3.set_title('Cumulative Patient Distribution', fontsize=14, fontweight='bold', pad=15)
    ax3.grid(alpha=0.3, linestyle='--')
    ax3.set_ylim([0, 105])
    
    # 4. Box plot
    ax4 = axes[1, 1]
    bp = ax4.boxplot([workload.values], vert=False, patch_artist=True,
                     boxprops=dict(facecolor='#4facfe', alpha=0.7, linewidth=2),
                     whiskerprops=dict(linewidth=2, color='#667eea'),
                     capprops=dict(linewidth=2, color='#667eea'),
                     medianprops=dict(linewidth=3, color='#fa709a'),
                     flierprops=dict(marker='o', markerfacecolor='#fa709a', markersize=8, alpha=0.7))
    
    ax4.set_xlabel('Number of Patients', fontsize=12, fontweight='bold')
    ax4.set_title('Workload Distribution (Box Plot)', fontsize=14, fontweight='bold', pad=15)
    ax4.grid(axis='x', alpha=0.3, linestyle='--')
    ax4.set_yticklabels(['All Doctors'])
    
    # Add statistics text
    stats_text = f"Min: {workload.min()}\nQ1: {workload.quantile(0.25):.1f}\nMedian: {workload.median():.1f}\nQ3: {workload.quantile(0.75):.1f}\nMax: {workload.max()}"
    ax4.text(0.02, 0.98, stats_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'doctor_workload_enhanced.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nSaved: doctor_workload_enhanced.png")
    plt.close()

def analyze_geographic_distribution(patients, branches):
    """Analyze geographic distribution with beautiful maps"""
    print("\n" + "="*70)
    print("GEOGRAPHIC DISTRIBUTION ANALYSIS")
    print("="*70)
    
    area_counts = patients['area'].value_counts()
    
    print(f"\nTotal areas served: {len(area_counts)}")
    print(f"\nTop 10 areas by patient volume:")
    for area, count in area_counts.head(10).items():
        print(f"  - {area}: {count} patients")
    
    # Create visualization
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('Geographic Distribution Dashboard', fontsize=20, fontweight='bold', y=0.995)
    
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # 1. Top areas - horizontal bars with gradient
    ax1 = fig.add_subplot(gs[0, 0])
    top_10_areas = area_counts.head(10)
    colors_gradient = plt.cm.turbo(np.linspace(0.1, 0.9, len(top_10_areas)))
    bars = ax1.barh(range(len(top_10_areas)), top_10_areas.values, color=colors_gradient, edgecolor='white', linewidth=2)
    ax1.set_yticks(range(len(top_10_areas)))
    ax1.set_yticklabels(top_10_areas.index, fontsize=11)
    ax1.set_xlabel('Number of Patients', fontsize=12, fontweight='bold')
    ax1.set_title('Top 10 Areas by Patient Volume', fontsize=14, fontweight='bold', pad=15)
    ax1.invert_yaxis()
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_10_areas.values)):
        ax1.text(value + 0.5, i, f'{value}', va='center', fontsize=10, fontweight='bold')
    
    # 2. Branch distribution - pie chart
    ax2 = fig.add_subplot(gs[0, 1])
    # Use branch_name directly from appointments
    branch_counts = patients['branch_name'].value_counts()
    
    colors_pie = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
    explode = [0.05] * min(len(branch_counts), 5)
    
    wedges, texts, autotexts = ax2.pie(
        branch_counts.values,
        labels=branch_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors_pie[:len(branch_counts)],
        explode=explode,
        shadow=True,
        textprops={'fontsize': 11, 'weight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
    
    ax2.set_title('Patient Distribution by Branch', fontsize=14, fontweight='bold', pad=15)
    
    # 3. All areas - vertical bars
    ax3 = fig.add_subplot(gs[1, :])
    all_areas = area_counts.head(20)
    colors_all = plt.cm.rainbow(np.linspace(0, 1, len(all_areas)))
    bars = ax3.bar(range(len(all_areas)), all_areas.values, color=colors_all, edgecolor='black', linewidth=1)
    ax3.set_xticks(range(len(all_areas)))
    ax3.set_xticklabels(all_areas.index, rotation=45, ha='right', fontsize=10)
    ax3.set_ylabel('Number of Patients', fontsize=12, fontweight='bold')
    ax3.set_title('Top 20 Areas - Complete Overview', fontsize=14, fontweight='bold', pad=15)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'geographic_distribution_enhanced.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nSaved: geographic_distribution_enhanced.png")
    plt.close()

def generate_summary_report(doctors, branches, diseases, patients):
    """Generate enhanced summary report"""
    print("\n" + "="*70)
    print("GENERATING ENHANCED SUMMARY REPORT")
    print("="*70)
    
    report = []
    report.append("="*80)
    report.append("SAYLANI MEDICAL HELP DESK - ENHANCED EDA SUMMARY REPORT")
    report.append("="*80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n" + "-"*80)
    report.append("DATASET OVERVIEW")
    report.append("-"*80)
    report.append(f"Total Doctors: {len(doctors)}")
    report.append(f"Total Branches: {len(branches)}")
    report.append(f"Total Diseases: {len(diseases)}")
    report.append(f"Total Patients: {len(patients)}")
    
    report.append("\n" + "-"*80)
    report.append("KEY STATISTICS")
    report.append("-"*80)
    
    # Disease stats
    disease_counts = patients['disease_name'].value_counts()
    report.append(f"\nMost common disease: {disease_counts.index[0]} ({disease_counts.iloc[0]} cases)")
    report.append(f"Unique diseases treated: {len(disease_counts)}")
    
    # Doctor stats
    workload = patients['doctor_name'].value_counts()
    report.append(f"\nAverage patients per doctor: {workload.mean():.1f}")
    report.append(f"Busiest doctor: {workload.index[0]} ({workload.iloc[0]} patients)")
    
    # Geographic stats
    area_counts = patients['area'].value_counts()
    report.append(f"\nAreas served: {len(area_counts)}")
    report.append(f"Most served area: {area_counts.index[0]} ({area_counts.iloc[0]} patients)")
    
    report.append("\n" + "="*80)
    report.append("ENHANCED VISUALIZATIONS GENERATED")
    report.append("="*80)
    report.append("disease_trends_enhanced.png")
    report.append("doctor_workload_enhanced.png")
    report.append("geographic_distribution_enhanced.png")
    
    report.append("\n" + "="*80)
    report.append("All visualizations feature beautiful color schemes and professional styling!")
    report.append("="*80)
    
    # Save report
    report_text = "\n".join(report)
    report_path = os.path.join(OUTPUT_DIR, 'eda_enhanced_summary.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\nSaved: eda_enhanced_summary.txt")

def generate_kb_insights(doctors, branches, diseases, patients):
    """Generate detailed analytics insights for the Knowledge Base"""
    print("\n" + "="*70)
    print("GENERATING KNOWLEDGE BASE INSIGHTS")
    print("="*70)
    
    kb_dir = "data/knowledge_base"
    os.makedirs(kb_dir, exist_ok=True)
    kb_path = os.path.join(kb_dir, "analytics_insights.md")
    
    with open(kb_path, "w", encoding="utf-8") as f:
        f.write("# Analytics Insights & Graph Explanations\n\n")
        f.write("This document contains interpretations of the analytics visualizations generated by the system. Use this to explain graphs and trends to the admin.\n\n")
        
        # 1. Disease Trends
        disease_counts = patients['disease_name'].value_counts()
        top_disease = disease_counts.index[0]
        top_count = disease_counts.iloc[0]
        
        f.write("## Disease Trends Analysis\n")
        f.write("### Overview\n")
        f.write(f"The disease trends analysis reveals that **{top_disease}** is the most prevalent condition, affecting {top_count} patients. ")
        f.write(f"In total, {len(disease_counts)} unique diseases were recorded.\n\n")
        
        f.write("### Top 10 Diseases Graph Interpretation\n")
        f.write("The 'Top 10 Most Common Diseases' bar chart shows the following distribution:\n")
        for disease, count in disease_counts.head(10).items():
            f.write(f"- **{disease}**: {count} cases\n")
        f.write("\nThis indicates a high prevalence of this specific set of diseases. The chart uses a gradient color scheme to highlight the most critical conditions.\n\n")
        
        f.write("### Disease Distribution Pie Chart\n")
        f.write("The pie chart illustrates the proportion of the top 5 diseases compared to all others. ")
        f.write(f"The top 5 diseases account for a significant portion of the total cases, highlighting the need to focus resources on these specific treatments.\n\n")

        # 2. Doctor Workload
        workload = patients['doctor_name'].value_counts()
        avg_load = workload.mean()
        busiest_doc_name = workload.index[0]
        
        f.write("## Doctor Workload Analysis\n")
        f.write("### Overview\n")
        f.write(f"The average workload per doctor is approximately **{avg_load:.1f} patients**. ")
        f.write(f"The busiest doctor is **{busiest_doc_name}** with {workload.iloc[0]} patients.\n\n")
        
        f.write("### Workload Distribution Graph Interpretation\n")
        f.write("The 'Doctor Workload Analysis' visualizations show a variance in patient distribution. ")
        f.write("The 'Top 10 Busiest Doctors' chart highlights those with the highest patient volume. ")
        f.write("The histogram and box plot show the spread of workload across all doctors, indicating whether the load is balanced or skewed.\n\n")
        
        # 3. Geographic Distribution
        area_counts = patients['area'].value_counts()
        top_area = area_counts.index[0]
        
        f.write("## Geographic Distribution Analysis\n")
        f.write("### Overview\n")
        f.write(f"Patients come from {len(area_counts)} different areas. ")
        f.write(f"The area with the highest patient volume is **{top_area}** with {area_counts.iloc[0]} patients.\n\n")
        
        f.write("### Geographic Charts Interpretation\n")
        f.write("The 'Geographic Distribution' charts highlight where the demand is coming from. ")
        f.write("The 'Top 10 Areas' bar chart identifies the primary catchment areas. ")
        f.write("The 'Patient Distribution by Branch' pie chart shows how patients are distributed across the different medical centers.\n\n")
        
        # 4. Temporal Trends (if available)
        if 'visit_timestamp' in patients.columns:
            patients['visit_date'] = pd.to_datetime(patients['visit_timestamp'], errors='coerce')
            daily_counts = patients.groupby(patients['visit_date'].dt.date).size()
            if not daily_counts.empty:
                peak_day = daily_counts.idxmax()
                peak_count = daily_counts.max()
                f.write("## Temporal Trends Analysis\n")
                f.write("### Patient Visits Over Time\n")
                f.write(f"The 'Patient Visits Over Time' line graph tracks the daily number of visits. ")
                f.write(f"The peak traffic was recorded on **{peak_day}** with {peak_count} visits. ")
                f.write("Monitoring these trends helps in staff scheduling and resource allocation.\n\n")

    print(f"Saved: {kb_path}")

def main():
    """Main EDA function"""
    print("\n" + "="*80)
    print("SAYLANI MEDICAL HELP DESK - ENHANCED EXPLORATORY DATA ANALYSIS")
    print("="*80)
    
    create_output_dir()
    
    # Load data
    doctors, branches, diseases, patients = load_data()
    
    # Run analyses with enhanced visualizations
    analyze_disease_trends(patients)
    analyze_doctor_workload(patients, doctors)
    analyze_geographic_distribution(patients, branches)
    
    # Generate summary
    generate_summary_report(doctors, branches, diseases, patients)
    
    # Generate Knowledge Base Insights
    generate_kb_insights(doctors, branches, diseases, patients)
    
    print("\n" + "="*80)
    print("ENHANCED EDA COMPLETE!")
    print("="*80)
    print(f"\nAll outputs saved to: {OUTPUT_DIR}")
    print("\nGenerated files with beautiful visualizations:")
    print("  disease_trends_enhanced.png")
    print("  doctor_workload_enhanced.png")
    print("  geographic_distribution_enhanced.png")
    print("  eda_enhanced_summary.txt")
    print("\nAll charts feature professional color schemes and styling!")
    print()

if __name__ == "__main__":
    main()
