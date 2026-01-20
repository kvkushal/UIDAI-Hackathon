"""
National-Level Analysis Plots for Aadhaar N.E.X.U.S Presentation
Generates 4 high-quality visualizations for the hackathon presentation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for presentation-quality plots
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Load data
df = pd.read_csv('data/district_equity_all_india.csv')
print(f"Loaded {len(df)} districts from {df['state'].nunique()} states/UTs")

# State-level aggregation
state_df = df.groupby('state').agg({
    'DEI': 'mean',
    'ASS': 'mean',
    'UBS': 'mean',
    'SRS': 'mean',
    'district': 'count'
}).rename(columns={'district': 'num_districts'}).reset_index()

# ==============================================================================
# PLOT 1: State DEI Ranking Bar Chart
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 10))

# Sort states by DEI
state_sorted = state_df.sort_values('DEI', ascending=True)

# Color based on DEI value
colors = ['#ef4444' if x < 0.7 else '#f59e0b' if x < 0.8 else '#22c55e' 
          for x in state_sorted['DEI']]

bars = ax1.barh(state_sorted['state'], state_sorted['DEI'], color=colors, edgecolor='white')

# Add national average line
national_avg = df['DEI'].mean()
ax1.axvline(national_avg, color='#3b82f6', linestyle='--', linewidth=2, label=f'National Avg: {national_avg:.3f}')

# Formatting
ax1.set_xlabel('Digital Equity Index (DEI)', fontweight='bold')
ax1.set_title('State/UT Rankings by Digital Equity Index', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlim(0.5, 1.0)
ax1.legend(loc='lower right', fontsize=11)

# Add value labels
for bar, val in zip(bars, state_sorted['DEI']):
    ax1.text(val + 0.005, bar.get_y() + bar.get_height()/2, f'{val:.3f}', 
             va='center', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/01_state_dei_ranking.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 1 saved: 01_state_dei_ranking.png")
plt.close()

# ==============================================================================
# PLOT 2: Risk Quadrant Scatter (All Districts)
# ==============================================================================
fig2, ax2 = plt.subplots(figsize=(12, 10))

scatter = ax2.scatter(
    df['UBS'], df['SRS'],
    c=df['DEI'],
    cmap='RdYlGn',
    s=50,
    alpha=0.7,
    edgecolors='white',
    linewidth=0.5
)

# Add quadrant lines
ax2.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

# Quadrant labels
ax2.text(0.15, 0.15, '✓ OPTIMAL\n(Low Burden, Low Risk)', fontsize=11, 
         ha='center', va='center', color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax2.text(0.85, 0.85, '⚠ RISK ZONE\n(High Burden, High Risk)', fontsize=11, 
         ha='center', va='center', color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax2.text(0.15, 0.85, 'Stability Issues\n(Low Burden, High Risk)', fontsize=10, 
         ha='center', va='center', color='#b45309', alpha=0.8)
ax2.text(0.85, 0.15, 'Update Overload\n(High Burden, Low Risk)', fontsize=10, 
         ha='center', va='center', color='#b45309', alpha=0.8)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax2, shrink=0.8)
cbar.set_label('DEI Score (Green = Better)', fontweight='bold')

ax2.set_xlabel('Update Burden Score (UBS) - Lower is Better', fontweight='bold')
ax2.set_ylabel('Stability Risk Score (SRS) - Lower is Better', fontweight='bold')
ax2.set_title(f'Risk Quadrant Analysis - All {len(df)} Districts', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('plots/02_risk_quadrant_scatter.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 2 saved: 02_risk_quadrant_scatter.png")
plt.close()

# ==============================================================================
# PLOT 3: DEI Distribution Histogram
# ==============================================================================
fig3, ax3 = plt.subplots(figsize=(12, 7))

# Histogram
n, bins, patches = ax3.hist(df['DEI'], bins=30, edgecolor='white', alpha=0.8, color='#6366f1')

# Color bars based on value
for i, patch in enumerate(patches):
    bin_center = (bins[i] + bins[i+1]) / 2
    if bin_center < 0.7:
        patch.set_facecolor('#ef4444')
    elif bin_center < 0.8:
        patch.set_facecolor('#f59e0b')
    else:
        patch.set_facecolor('#22c55e')

# Add reference lines
ax3.axvline(national_avg, color='#3b82f6', linestyle='-', linewidth=3, 
            label=f'National Average: {national_avg:.3f}')

# Top/Bottom states
top_states = state_df.nlargest(3, 'DEI')['DEI'].mean()
bottom_states = state_df.nsmallest(3, 'DEI')['DEI'].mean()

ax3.axvline(top_states, color='#22c55e', linestyle='--', linewidth=2, 
            label=f'Top 3 States Avg: {top_states:.3f}')
ax3.axvline(bottom_states, color='#ef4444', linestyle='--', linewidth=2, 
            label=f'Bottom 3 States Avg: {bottom_states:.3f}')

ax3.set_xlabel('Digital Equity Index (DEI)', fontweight='bold')
ax3.set_ylabel('Number of Districts', fontweight='bold')
ax3.set_title('Distribution of DEI Scores Across All Districts', fontsize=16, fontweight='bold', pad=20)
ax3.legend(loc='upper left', fontsize=11)

# Add stats box
stats_text = f'Total Districts: {len(df)}\nMean: {df["DEI"].mean():.3f}\nStd: {df["DEI"].std():.3f}'
ax3.text(0.98, 0.95, stats_text, transform=ax3.transAxes, fontsize=11,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

plt.tight_layout()
plt.savefig('plots/03_dei_distribution.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 3 saved: 03_dei_distribution.png")
plt.close()

# ==============================================================================
# PLOT 4: State Box Plot (DEI Variance by State)
# ==============================================================================
fig4, ax4 = plt.subplots(figsize=(14, 8))

# Get state order by median DEI
state_order = df.groupby('state')['DEI'].median().sort_values(ascending=False).index

# Create box plot
bp = ax4.boxplot([df[df['state'] == s]['DEI'].values for s in state_order],
                  labels=state_order,
                  patch_artist=True,
                  vert=False)

# Color boxes by median
medians = [df[df['state'] == s]['DEI'].median() for s in state_order]
colors = ['#22c55e' if m >= 0.8 else '#f59e0b' if m >= 0.7 else '#ef4444' for m in medians]

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# National average line
ax4.axvline(national_avg, color='#3b82f6', linestyle='--', linewidth=2, 
            label=f'National Avg: {national_avg:.3f}')

ax4.set_xlabel('Digital Equity Index (DEI)', fontweight='bold')
ax4.set_title('DEI Distribution Within Each State/UT', fontsize=16, fontweight='bold', pad=20)
ax4.legend(loc='lower right', fontsize=11)
ax4.set_xlim(0.3, 1.0)

plt.tight_layout()
plt.savefig('plots/04_state_boxplot.png', bbox_inches='tight', facecolor='white')
print("✅ Plot 4 saved: 04_state_boxplot.png")
plt.close()

print("\n" + "="*60)
print("🎉 All 4 plots generated successfully!")
print("📁 Saved in: uidai_dashboard/plots/")
print("="*60)
