"""
Generate District Intervention Mapping Table for Andhra Pradesh
As requested: A simple, actionable table (not a chart).
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

# Load data
df = pd.read_csv('data/district_equity_all_india.csv')
ap = df[df['state'] == 'Andhra Pradesh'].copy()
ap['district'] = ap['district'].str.title()

# Define logic for Dominant Risk & Action
def get_intervention(row):
    # Critical Quality (Low DEI) - Check specific sub-metrics
    if row['DEI'] < 0.7:
        if row['AHS'] < 0.5 and row['SRS'] > 0.6:
            return 'Access + Stability Crisis', 'Urgent: New centers + Infra audit'
        elif row['AHS'] < 0.6:
            return 'Severe Access Deficit', 'Deploy mobile vans + New centers'
        elif row['SRS'] > 0.6:
            return 'High Stability Risk', 'Technical audit + Connectivity upgrade'
        else:
            return 'General Quality Critical', 'Complete district review required'
            
    # Warning Zone - Identifying specific stressors
    elif row['DEI'] < 0.8:
        if row['UBS'] > 0.6:
            return 'High Update Burden', 'Setup dedicated update camps'
        elif row['AHS'] < 0.7:
            return 'Moderate Access Stress', 'Extend center operating hours'
        else:
            return 'Borderline Performance', 'Monitor weekly + Staff training'
            
    # Good Performance
    else:
        return 'Healthy State', 'Reference model for other districts'

# Apply logic
ap[['Dominant Risk', 'Suggested Action']] = ap.apply(
    lambda x: pd.Series(get_intervention(x)), axis=1
)

# Sort by DEI (ascending) to show critical ones first
table_df = ap.sort_values('DEI')[['district', 'Dominant Risk', 'Suggested Action']]

# Rename columns for display
table_df.columns = ['District', 'Dominant Risk', 'Suggested Action']

# ==============================================================================
# RENDER AS TABLE IMAGE
# ==============================================================================
# ==============================================================================
# SELECT REPRESENTATIVE DISTRICTS (Worst, Mid, Best)
# ==============================================================================
# Sort the original 'ap' dataframe by DEI
ap_sorted = ap.sort_values('DEI')

best_district = ap_sorted.iloc[-1:]  # Highest DEI
worst_district = ap_sorted.iloc[:1]  # Lowest DEI
mid_index = len(ap_sorted) // 2
mid_district = ap_sorted.iloc[mid_index:mid_index+1] # Median DEI

# Concatenate in logical order: Worst -> Mid -> Best
display_df = pd.concat([worst_district, mid_district, best_district])

# Select only the display columns
display_df = display_df[['district', 'Dominant Risk', 'Suggested Action']]
display_df.columns = ['District', 'Dominant Risk', 'Suggested Action']

# Create figure
fig, ax = plt.subplots(figsize=(12, 2.5)) # Reduced height for just 3 rows
ax.axis('off')

# Table styling
table = ax.table(
    cellText=display_df.values,
    colLabels=display_df.columns,
    cellLoc='left',
    loc='center',
    colColours=['#1e3a5f']*3
)

# Adjust table properties
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8) # Stretch height

# Column widths
table.auto_set_column_width([0, 1, 2])

# Styling cells
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(color='white', weight='bold')
        cell.set_edgecolor('white')
    else:
        cell.set_edgecolor('#e5e7eb')
        cell.set_text_props(color='#1f2937')
        
        # Color code risk column
        risk_text = display_df.iloc[row-1, 1]
        if 'Critical' in risk_text or 'Crisis' in risk_text or 'Severe' in risk_text:
            if col == 1: cell.set_text_props(color='#ef4444', weight='bold')
        elif 'Healthy' in risk_text:
            if col == 1: cell.set_text_props(color='#22c55e', weight='bold')

plt.title('District Intervention Mapping Table (Andhra Pradesh Selection)', 
          fontsize=14, weight='bold', pad=10, color='#111827')

plt.tight_layout()
plt.savefig('plots/andhra_pradesh/06_ap_intervention_table.png', bbox_inches='tight', dpi=300)
print("✅ Table saved: plots/andhra_pradesh/06_ap_intervention_table.png")

# Also save full CSV logic
table_df.to_csv('plots/andhra_pradesh/ap_intervention_logic.csv', index=False)
print("✅ Full logic CSV saved")
