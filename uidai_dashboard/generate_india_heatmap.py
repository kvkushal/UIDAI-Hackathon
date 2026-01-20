"""
Generate All India Heatmap as high-quality PNG for presentation
"""
import pandas as pd
import plotly.express as px
import requests
import json

# Load data
df = pd.read_csv('data/district_equity_all_india.csv')

# State-level aggregation
state_df = df.groupby('state').agg({
    'DEI': 'mean',
    'district': 'count'
}).reset_index()

# Fix state name for GeoJSON matching
state_name_mapping = {
    'Jammu and Kashmir': 'Jammu & Kashmir',
}
state_df['state'] = state_df['state'].replace(state_name_mapping)

# Load GeoJSON
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
r = requests.get(url, timeout=60)
geojson_data = r.json()

# Create choropleth
fig = px.choropleth(
    state_df,
    geojson=geojson_data,
    locations='state',
    featureidkey='properties.ST_NM',
    color='DEI',
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=state_df['DEI'].mean(),
    range_color=[state_df['DEI'].min(), state_df['DEI'].max()],
    hover_name='state',
    hover_data={'DEI': ':.3f', 'district': True},
    labels={'DEI': 'DEI (Higher = Better)', 'district': 'Districts'},
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor='white'
)

fig.update_layout(
    title={
        'text': 'The National Pulse: State-wise Digital Equity Index',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'family': 'Arial Black', 'color': '#1e3a5f'}
    },
    height=800,
    width=1000,
    margin=dict(l=20, r=20, t=80, b=20),
    paper_bgcolor='white',
    geo=dict(bgcolor='white'),
    coloraxis_colorbar=dict(
        title="DEI Score",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.92,
        len=0.6
    )
)

# Save as high-quality PNG
fig.write_image("plots/08_india_heatmap_hq.png", scale=3)
print("✅ Saved: plots/08_india_heatmap_hq.png (High Resolution)")

# Also save an SVG for even higher quality
fig.write_image("plots/08_india_heatmap.svg")
print("✅ Saved: plots/08_india_heatmap.svg (Vector)")

print(f"\n📊 Map shows {len(state_df)} states/UTs")
print(f"📌 National Avg DEI: {state_df['DEI'].mean():.3f}")
