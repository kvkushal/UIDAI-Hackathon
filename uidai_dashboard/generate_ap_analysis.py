"""
Andhra Pradesh State Analysis - Complete Visualization Suite
Generates all plots for hackathon presentation
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create AP plots folder
os.makedirs('plots/andhra_pradesh', exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

# Load data
df = pd.read_csv('data/district_equity_all_india.csv')
ap = df[df['state'] == 'Andhra Pradesh'].copy()
ap['district'] = ap['district'].str.title()

print(f"Andhra Pradesh: {len(ap)} districts")
print(f"Avg DEI: {ap['DEI'].mean():.3f}")

# Categorize districts
def categorize(dei):
    if dei >= 0.8: return 'Good'
    elif dei >= 0.7: return 'Warning'
    else: return 'Critical'

ap['Category'] = ap['DEI'].apply(categorize)

# ==============================================================================
# PLOT 1: District DEI Ranking Bar Chart
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 10))
ap_sorted = ap.sort_values('DEI', ascending=True)

colors = ['#ef4444' if c == 'Critical' else '#f59e0b' if c == 'Warning' else '#22c55e' 
          for c in ap_sorted['Category']]

bars = ax1.barh(ap_sorted['district'], ap_sorted['DEI'], color=colors, edgecolor='white')

# State avg line
state_avg = ap['DEI'].mean()
ax1.axvline(state_avg, color='#3b82f6', linestyle='--', linewidth=2, label=f'State Avg: {state_avg:.3f}')

ax1.set_xlabel('Digital Equity Index (DEI)', fontweight='bold', fontsize=12)
ax1.set_title('Andhra Pradesh - District DEI Rankings', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlim(0.3, 1.0)
ax1.legend(loc='lower right', fontsize=11)

# Add value labels
for bar, val in zip(bars, ap_sorted['DEI']):
    ax1.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.3f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('plots/andhra_pradesh/01_ap_district_ranking.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 1: District DEI Ranking")
plt.close()

# ==============================================================================
# PLOT 2: Risk Quadrant Scatter
# ==============================================================================
fig2, ax2 = plt.subplots(figsize=(10, 8))

scatter = ax2.scatter(ap['UBS'], ap['SRS'], c=ap['DEI'], cmap='RdYlGn', s=150, 
                       edgecolors='white', linewidth=1.5)

# Add district labels
for _, row in ap.iterrows():
    ax2.annotate(row['district'][:8], (row['UBS'], row['SRS']), fontsize=7, 
                 ha='center', va='bottom', alpha=0.8)

ax2.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
ax2.axvline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

ax2.text(0.15, 0.15, '✓ OPTIMAL', fontsize=12, ha='center', color='green', fontweight='bold')
ax2.text(0.85, 0.85, '⚠ RISK', fontsize=12, ha='center', color='red', fontweight='bold')

cbar = plt.colorbar(scatter, ax=ax2, shrink=0.8)
cbar.set_label('DEI Score', fontweight='bold')

ax2.set_xlabel('Update Burden Score (UBS)', fontweight='bold')
ax2.set_ylabel('Stability Risk Score (SRS)', fontweight='bold')
ax2.set_title('Andhra Pradesh - Risk Quadrant Analysis', fontsize=14, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('plots/andhra_pradesh/02_ap_risk_quadrant.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 2: Risk Quadrant")
plt.close()

# ==============================================================================
# PLOT 3: Category Distribution (Pie + Bar)
# ==============================================================================
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))

cat_counts = ap['Category'].value_counts()
colors_cat = {'Good': '#22c55e', 'Warning': '#f59e0b', 'Critical': '#ef4444'}

# Donut chart
wedges, texts, autotexts = ax3a.pie(
    [cat_counts.get('Good', 0), cat_counts.get('Warning', 0), cat_counts.get('Critical', 0)],
    labels=['Good', 'Warning', 'Critical'],
    colors=[colors_cat['Good'], colors_cat['Warning'], colors_cat['Critical']],
    autopct='%1.0f%%',
    wedgeprops=dict(width=0.5, edgecolor='white'),
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
ax3a.text(0, 0, f'{len(ap)}\nDistricts', ha='center', va='center', fontsize=14, fontweight='bold')
ax3a.set_title('District Distribution', fontsize=14, fontweight='bold')

# Bar chart
categories = ['Good', 'Warning', 'Critical']
counts = [cat_counts.get(c, 0) for c in categories]
bars = ax3b.bar(categories, counts, color=[colors_cat[c] for c in categories], edgecolor='white', linewidth=2)
for bar, count in zip(bars, counts):
    ax3b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(count), 
              ha='center', fontsize=14, fontweight='bold')
ax3b.set_ylabel('Number of Districts', fontweight='bold')
ax3b.set_title('Districts by Performance Category', fontsize=14, fontweight='bold')

plt.suptitle('Andhra Pradesh - Performance Overview', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/andhra_pradesh/03_ap_category_distribution.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 3: Category Distribution")
plt.close()

# ==============================================================================
# PLOT 4: Multi-Metric Comparison (Top 5 vs Bottom 5)
# ==============================================================================
fig4, axes = plt.subplots(2, 2, figsize=(12, 10))

top5 = ap.nlargest(5, 'DEI')
bottom5 = ap.nsmallest(5, 'DEI')

metrics = [('DEI', 'Digital Equity Index', True),
           ('AHS', 'Access Health Score', True),
           ('UBS', 'Update Burden Score', False),
           ('SRS', 'Stability Risk Score', False)]

for ax, (metric, title, higher_better) in zip(axes.flatten(), metrics):
    y_pos = np.arange(5)
    
    ax.barh(y_pos + 0.2, top5[metric].values, 0.35, label='Top 5', color='#22c55e', alpha=0.8)
    ax.barh(y_pos - 0.2, bottom5[metric].values, 0.35, label='Bottom 5', color='#ef4444', alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([d[:12] for d in top5['district'].values], fontsize=9)
    ax.set_xlabel(metric, fontweight='bold')
    subtitle = '(Higher = Better)' if higher_better else '(Lower = Better)'
    ax.set_title(f'{title}\n{subtitle}', fontsize=11, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)

plt.suptitle('Andhra Pradesh - Top 5 vs Bottom 5 Districts', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/andhra_pradesh/04_ap_top_vs_bottom.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 4: Top 5 vs Bottom 5")
plt.close()

# ==============================================================================
# PLOT 5: Metric Heatmap (All Districts x All Metrics)
# ==============================================================================
fig5, ax5 = plt.subplots(figsize=(10, 12))

heatmap_data = ap.set_index('district')[['DEI', 'AHS', 'UBS', 'SRS']].sort_values('DEI', ascending=False)

# Normalize for visualization
normalized = heatmap_data.copy()
for col in normalized.columns:
    if col in ['UBS', 'SRS']:  # Lower is better, so invert
        normalized[col] = 1 - normalized[col]

sns.heatmap(normalized, annot=heatmap_data.round(2), cmap='RdYlGn', center=0.5,
            linewidths=0.5, fmt='', ax=ax5, cbar_kws={'label': 'Performance (Green = Better)'})

ax5.set_title('Andhra Pradesh - District Performance Heatmap\n(All Metrics)', fontsize=14, fontweight='bold')
ax5.set_xlabel('Metric', fontweight='bold')
ax5.set_ylabel('District', fontweight='bold')

plt.tight_layout()
plt.savefig('plots/andhra_pradesh/05_ap_heatmap.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 5: Performance Heatmap")
plt.close()

# ==============================================================================
# SAVE DATA TABLE AS CSV
# ==============================================================================
ap_table = ap[['district', 'DEI', 'AHS', 'UBS', 'SRS', 'Category']].sort_values('DEI', ascending=False)
ap_table.to_csv('plots/andhra_pradesh/ap_district_scores.csv', index=False)
print("✅ Table: ap_district_scores.csv")

# ==============================================================================
# SUMMARY STATS
# ==============================================================================
print("\n" + "="*60)
print("📊 ANDHRA PRADESH ANALYSIS COMPLETE")
print("="*60)
print(f"Total Districts: {len(ap)}")
print(f"State Avg DEI: {ap['DEI'].mean():.3f}")
print(f"🟢 Good (DEI ≥ 0.8): {len(ap[ap['DEI'] >= 0.8])}")
print(f"🟡 Warning (0.7-0.8): {len(ap[(ap['DEI'] >= 0.7) & (ap['DEI'] < 0.8)])}")
print(f"🔴 Critical (< 0.7): {len(ap[ap['DEI'] < 0.7])}")
print(f"\nBest District: {ap.loc[ap['DEI'].idxmax(), 'district']} ({ap['DEI'].max():.3f})")
print(f"Worst District: {ap.loc[ap['DEI'].idxmin(), 'district']} ({ap['DEI'].min():.3f})")
print("\n📁 All plots saved in: plots/andhra_pradesh/")
