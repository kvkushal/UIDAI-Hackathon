"""
Merge Madhya Pradesh district scores into district_equity_all_india.csv
"""
import pandas as pd
import os

# Paths
BASE_PATH = r"c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon"
MASTER_CSV = os.path.join(BASE_PATH, "uidai_dashboard", "data", "district_equity_all_india.csv")
MP_CSV = os.path.join(BASE_PATH, "East", "Madhya pradesh", "madhya_pradesh_district_final_scores.csv")

# Load data
master_df = pd.read_csv(MASTER_CSV)
mp_df = pd.read_csv(MP_CSV)

print(f"Master rows before: {len(master_df)}")
print(f"MP rows to add: {len(mp_df)}")

# Remove any existing "Madhya Pradesh" rows (idempotency)
master_df = master_df[master_df['state'] != 'Madhya Pradesh']
print(f"Master rows after removing existing MP: {len(master_df)}")

# Concatenate
merged_df = pd.concat([master_df, mp_df], ignore_index=True)

# Sort by state, then district
merged_df = merged_df.sort_values(['state', 'district']).reset_index(drop=True)

print(f"Master rows after merge: {len(merged_df)}")

# Save
merged_df.to_csv(MASTER_CSV, index=False)
print(f"✅ Saved to {MASTER_CSV}")

# Verify MP is present
mp_count = len(merged_df[merged_df['state'] == 'Madhya Pradesh'])
print(f"✅ Madhya Pradesh districts in final file: {mp_count}")
