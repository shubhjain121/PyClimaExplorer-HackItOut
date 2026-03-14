# app.py – PyClimaExplorer: Multi-Dataset Climate Dashboard
import streamlit as st
import xarray as xr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="PyClimaExplorer", layout="wide", page_icon="🌍")

st.markdown("""
<style>
/* Force High-Contrast Light Theme (White Background, Black Text) */
.stApp, .main, header[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

/* Global Text Visibility - Black on White */
html, body, [class*="css"], .stMarkdown, p, span, label, li {
    font-family: Georgia, serif;
    color: #000000 !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
    font-family: Georgia, serif;
}

/* Sidebar Styling - Yellow background */
div[data-testid="stSidebar"] {
    background-color: #FFD700 !important;
}

/* ── Sidebar: ALL text white ── */
div[data-testid="stSidebar"],
div[data-testid="stSidebar"] *,
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3,
div[data-testid="stSidebar"] h4,
div[data-testid="stSidebar"] h5,
div[data-testid="stSidebar"] h6,
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] span,
div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] div,
div[data-testid="stSidebar"] li,
div[data-testid="stSidebar"] a,
div[data-testid="stSidebar"] small,
div[data-testid="stSidebar"] .stMarkdown,
div[data-testid="stSidebar"] .stCaption,
div[data-testid="stSidebar"] .stRadio label,
div[data-testid="stSidebar"] .stRadio div,
div[data-testid="stSidebar"] .stRadio span,
div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stSelectbox div,
div[data-testid="stSidebar"] .stSelectbox span,
div[data-testid="stSidebar"] .stSlider label,
div[data-testid="stSidebar"] .stSlider div,
div[data-testid="stSidebar"] .stSlider span,
div[data-testid="stSidebar"] .stNumberInput label,
div[data-testid="stSidebar"] .stNumberInput div,
div[data-testid="stSidebar"] .stNumberInput span,
div[data-testid="stSidebar"] .stTextInput label,
div[data-testid="stSidebar"] .stTextInput div,
div[data-testid="stSidebar"] .stTextInput span,
div[data-testid="stSidebar"] [data-testid="stTickBarMin"],
div[data-testid="stSidebar"] [data-testid="stTickBarMax"],
div[data-testid="stSidebar"] [data-testid="stSliderTick"],
div[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
    color: #ffffff !important;
}

/* Sidebar selectbox dropdown value text */
div[data-testid="stSidebar"] [data-baseweb="select"] [class*="ValueContainer"] *,
div[data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"],
div[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"] {
    color: #ffffff !important;
}

/* Sidebar number input text */
div[data-testid="stSidebar"] input {
    color: #ffffff !important;
    background-color: #2e2e2e !important;
    border-color: #555555 !important;
}

/* Sidebar radio button text */
div[data-testid="stSidebar"] [data-testid="stRadio"] label p,
div[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    color: #ffffff !important;
}

/* Specific UI Elements outside sidebar */
.stCaption { color: #333333 !important; }
[data-testid="stMetricValue"] { color: #000000 !important; }
[data-testid="stMetricLabel"] { color: #000000 !important; }

/* Sliders and Selectboxes outside sidebar stay black */
.stSlider label, .stSelectbox label {
    color: #000000 !important;
}

/* Buttons */
.stButton button {
    color: #000000 !important;
    border-color: #000000 !important;
    background-color: #ffffff !important;
}

.section {
    border-bottom: 2px solid #000000;
    padding-bottom: 4px;
    margin: 20px 0 10px 0;
    font-size: 1.15rem;
    font-weight: bold;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Dataset Registry ──────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

DATASETS = {
    "Air Temperature (NCEP)":   {"file": "air.mon.mean.nc",   "var": "air",   "unit": "C",       "label": "Temperature (C)",   "scale": 1.0},
    "Wind Speed U-component":   {"file": "uwnd.mon.mean.nc",  "var": "uwnd",  "unit": "m/s",     "label": "U-Wind (m/s)",       "scale": 1.0},
    "Precipitation Rate":       {"file": "sample_data.nc",    "var": "prate", "unit": "mm/day",  "label": "Precip (mm/day)",    "scale": 86400.0},
}

@st.cache_data
def load_nc(filename, scale=1.0):
    path = os.path.join(DATA_DIR, filename)
    ds = xr.open_dataset(path)
    return ds, scale

# Pre-load all datasets at startup (uses cache after first load)
all_ds = {name: load_nc(info["file"], info["scale"]) for name, info in DATASETS.items()}

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🌍 PyClimaExplorer")
st.caption("Multi-dataset interactive climate visualizer · NCEP Reanalysis 1948–2026")

# Quick stats
c1, c2, c3, c4 = st.columns(4)
c1.metric("Datasets Loaded", "3")
c2.metric("Time Coverage", "1948 – 2026")
c3.metric("Variables", "Temperature · Wind · Precipitation")
c4.metric("Time Steps", "938 months")
st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Controls")
view = st.sidebar.radio("View", [
    "Global Heatmap",
    "Time Series",
    "Dataset Comparison",
    "Side-by-Side Years"
])

dataset_name = st.sidebar.selectbox("Dataset", list(DATASETS.keys()))
info        = DATASETS[dataset_name]
ds, _scale  = all_ds[dataset_name]
var  = info["var"]
unit = info["unit"]

# Time selection
times = pd.DatetimeIndex(ds['time'].values)
years = sorted(times.year.unique())

if view in ["Global Heatmap", "Side-by-Side Years"]:
    sel_year  = st.sidebar.slider("Year", int(years[0]), int(years[-1]), int(years[-1]))
    sel_month = st.sidebar.select_slider("Month", list(range(1, 13)),
                                          format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                   "Jul","Aug","Sep","Oct","Nov","Dec"][m-1])


# ── Helper functions ──────────────────────────────────────────────────────────
def get_slice(dataset, variable, year, month, scale=1.0):
    """Get a single month's lat/lon slice, applying unit scale."""
    t  = dataset.sel(time=f"{year}-{month:02d}", method="nearest")
    da = t[variable] * scale
    return da

def slice_to_df(data_array, var_name):
    """Convert 2D DataArray to a DataFrame for plotting."""
    df = data_array.to_dataframe().reset_index().dropna(subset=[var_name])
    return df

def global_mean_timeseries(dataset, variable):
    """Return a DataFrame with monthly global mean over time."""
    gmean = dataset[variable].mean(dim=['lat', 'lon'])
    df = gmean.to_dataframe().reset_index()
    df['time'] = pd.to_datetime(df['time'])
    return df

def annual_mean_timeseries(dataset, variable):
    """Return annual mean time series."""
    df = global_mean_timeseries(dataset, variable)
    df['year'] = df['time'].dt.year
    return df.groupby('year')[variable].mean().reset_index()

def get_color_config(var_name, df, col):
    """
    Return (colorscale, vmin, vmax) appropriate for the variable type.
    - Temperature (air): RdBu_r, quantile range
    - Wind (uwnd):  RdBu_r diverging, symmetric ±bound around 0
    - Precipitation (prate): Blues, 0 = white, heavy rain = dark blue
    """
    q02 = float(df[col].quantile(0.02))
    q98 = float(df[col].quantile(0.98))

    if var_name == 'uwnd':
        bound = max(abs(q02), abs(q98))
        return 'RdBu_r', -bound, bound
    elif var_name == 'prate':
        # Blues: 0 rain = very light, heavy rain = dark blue
        # Start from 0 always so dry areas are clearly white/light
        return 'Blues', 0.0, max(q98, 1.0)
    else:
        return 'RdBu_r', q02, q98

# ════════════════════════════════════════════════════════════════════
# VIEW 1 – Global Heatmap
# ════════════════════════════════════════════════════════════════════
if view == "Global Heatmap":
    st.markdown(f'<div class="section">Global Heatmap — {dataset_name}</div>', unsafe_allow_html=True)
    st.caption(f"Showing {sel_year}-{sel_month:02d}. Each dot is one grid cell. Drag to pan, scroll to zoom.")

    try:
        scale  = info["scale"]
        sliced = get_slice(ds, var, sel_year, sel_month, scale)
        df_map = slice_to_df(sliced, var)

        cscale, vmin, vmax = get_color_config(var, df_map, var)

        fig = px.scatter_geo(
            df_map, lat='lat', lon='lon', color=var,
            color_continuous_scale=cscale,
            range_color=[vmin, vmax],
            projection='natural earth',
            labels={var: unit},
            title=f"{dataset_name} — {sel_year}/{sel_month:02d}",
            hover_data={'lat': ':.1f', 'lon': ':.1f', var: ':.2f'}
        )
        fig.update_traces(marker=dict(size=3, opacity=1.0))
        fig.update_layout(
            height=520, paper_bgcolor='#faf9f6',
            font=dict(family='Georgia', color='#2c2c2c'),
            coloraxis_colorbar=dict(
                title=dict(text=unit, font=dict(color='#2c2c2c', size=12)),
                tickfont=dict(color='#2c2c2c', size=11),
                outlinewidth=1, outlinecolor='#c8a97e'
            ),
            geo=dict(
                bgcolor='#faf9f6', showocean=True, oceancolor='#c9dff0',
                showland=True, landcolor='#e6ddd0',
                showcoastlines=True, coastlinecolor='#7a6a56', showframe=False,

            )
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)

        # ── Annual Trend ──
        st.markdown('<div class="section">Global Context & Seasonal Cycle</div>', unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns([2, 1])
        
        with col_t1:
            ann_df = annual_mean_timeseries(ds, var)
            ann_df[var] *= scale
            
            fig2 = px.line(ann_df, x='year', y=var,
                             labels={'year': 'Year', var: unit},
                             title=f"Annual Global Mean (1948–2026)")
            trend = np.poly1d(np.polyfit(ann_df['year'], ann_df[var], 1))(ann_df['year'])
            fig2.add_trace(go.Scatter(x=ann_df['year'], y=trend, mode='lines',
                                      name='Long-term Trend', line=dict(color='#c0392b', dash='dash', width=2)))
            fig2.add_vline(x=sel_year, line_width=2, line_dash="dash", line_color="#1e8449")
            fig2.update_layout(height=350, paper_bgcolor='#faf9f6', plot_bgcolor='#fffef9',
                               font=dict(family='Georgia', color='#2c2c2c'),
                               xaxis=dict(gridcolor='#ede8df'), yaxis=dict(gridcolor='#ede8df'),
                               margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig2, use_container_width=True, theme=None)

        with col_t2:
            # Monthly data for THIS specific year
            this_year_ds = ds[var].sel(time=slice(f"{sel_year}-01", f"{sel_year}-12"))
            this_year_mean = this_year_ds.mean(dim=['lat', 'lon']) * scale
            m_df = this_year_mean.to_dataframe().reset_index()
            m_df['Month'] = pd.to_datetime(m_df['time']).dt.strftime('%b')
            
            fig_month = px.bar(m_df, x='Month', y=var,
                               title=f"Monthly Cycle in {sel_year}",
                               labels={var: unit},
                               color_discrete_sequence=['#c8a97e'])
            fig_month.update_layout(height=350, paper_bgcolor='#faf9f6', plot_bgcolor='#fffef9',
                                    font=dict(family='Georgia', color='#2c2c2c'),
                                    xaxis=dict(gridcolor='#ede8df'), yaxis=dict(gridcolor='#ede8df'),
                                    margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_month, use_container_width=True, theme=None)

    except Exception as e:
        st.error(f"Could not render visualizations: {e}")

# ════════════════════════════════════════════════════════════════════
# VIEW 2 – Time Series
# ════════════════════════════════════════════════════════════════════
elif view == "Time Series":
    st.markdown(f'<div class="section">Time Series — {dataset_name}</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    lat_in = col_a.number_input("Latitude",  -90.0,  90.0,  20.0, step=5.0)
    lon_in = col_b.number_input("Longitude", -180.0, 180.0, 78.0, step=5.0)

    year_range = st.slider("Year range", int(years[0]), int(years[-1]),
                           (int(years[0]), int(years[-1])))

    # Location time series
    point = ds[var].sel(lat=lat_in, lon=lon_in, method='nearest')
    df_ts = point.to_dataframe().reset_index()
    df_ts['time'] = pd.to_datetime(df_ts['time'])
    mask  = (df_ts['time'].dt.year >= year_range[0]) & (df_ts['time'].dt.year <= year_range[1])
    df_ts = df_ts[mask]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_ts['time'], y=df_ts[var], mode='lines',
                               name=f'{dataset_name}',
                               line=dict(color='#2471a3', width=1.5),
                               fill='tozeroy', fillcolor='rgba(36,113,163,0.07)'))

    # Overlay 12-month rolling mean
    df_ts['rolling'] = df_ts[var].rolling(12, center=True).mean()
    fig3.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['rolling'], mode='lines',
                               name='12-month mean',
                               line=dict(color='#c0392b', width=2)))

    fig3.update_layout(
        height=400,
        title=f"{dataset_name} at ({lat_in:.1f}°, {lon_in:.1f}°) — {year_range[0]} to {year_range[1]}",
        paper_bgcolor='#faf9f6', plot_bgcolor='#fffef9',
        font=dict(family='Georgia', color='#2c2c2c'),
        xaxis=dict(title='Date', gridcolor='#ede8df'),
        yaxis=dict(title=unit, gridcolor='#ede8df'),
        legend=dict(bgcolor='#fef9f2', bordercolor='#e0d0bb')
    )
    st.plotly_chart(fig3, use_container_width=True, theme=None)

    # Stats
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Mean",  f"{df_ts[var].mean():.2f} {unit}")
    sc2.metric("Min",   f"{df_ts[var].min():.2f} {unit}")
    sc3.metric("Max",   f"{df_ts[var].max():.2f} {unit}")

    with st.expander("Raw monthly data"):
        st.dataframe(df_ts[['time', var]].set_index('time').rename(columns={var: unit}))

# ════════════════════════════════════════════════════════════════════
# VIEW 3 – Dataset Comparison (all 3 on one chart)
# ════════════════════════════════════════════════════════════════════
elif view == "Dataset Comparison":
    st.markdown('<div class="section">All-Dataset Annual Mean Comparison</div>', unsafe_allow_html=True)
    st.caption("Annual global mean for all three variables plotted together (normalised to z-scores for comparability).")

    colors = {'Air Temperature (NCEP)': '#c0392b',
              'Wind Speed U-component': '#2471a3',
              'Precipitation Rate':     '#1e8449'}

    fig4 = go.Figure()
    for dname, dinfo in DATASETS.items():
        d, s  = all_ds[dname]
        v     = dinfo["var"]
        ann   = annual_mean_timeseries(d, v)
        val   = ann[v] * s  # Apply unit scaling
        zscore = (val - val.mean()) / val.std()
        fig4.add_trace(go.Scatter(
            x=ann['year'], y=zscore, mode='lines',
            name=dname,
            line=dict(color=colors[dname], width=2)
        ))

    fig4.add_hline(y=0, line_color='#c8b89a', line_dash='dot')
    fig4.update_layout(
        height=430,
        title="Normalised Annual Global Mean — Temperature vs Wind vs Precipitation (1948–2026)",
        paper_bgcolor='#faf9f6', plot_bgcolor='#fffef9',
        font=dict(family='Georgia', color='#2c2c2c'),
        xaxis=dict(title='Year', gridcolor='#ede8df'),
        yaxis=dict(title='Z-score (std deviations from mean)', gridcolor='#ede8df'),
        legend=dict(bgcolor='#fef9f2', bordercolor='#e0d0bb', borderwidth=1)
    )
    st.plotly_chart(fig4, use_container_width=True, theme=None)

    # Correlation table
    st.markdown('<div class="section">Correlation Matrix</div>', unsafe_allow_html=True)
    combined = {}
    for dname, dinfo in DATASETS.items():
        d, s   = all_ds[dname]
        v   = dinfo["var"]
        ann = annual_mean_timeseries(d, v)
        combined[dname] = ann[v].values * s

    min_len = min(len(v) for v in combined.values())
    corr_df = pd.DataFrame({k: v[:min_len] for k, v in combined.items()}).corr().round(3)
    
    fig_corr = px.imshow(corr_df,
                         text_auto=True,
                         aspect="auto",
                         color_continuous_scale='RdYlGn',
                         range_color=[-1, 1],
                         labels=dict(color="Correlation"),
                         title="Correlation between Temperature, Wind, and Precipitation")
    
    fig_corr.update_layout(height=400, paper_bgcolor='#faf9f6', plot_bgcolor='#fffef9',
                           font=dict(family='Georgia', color='#2c2c2c'))
    st.plotly_chart(fig_corr, use_container_width=True, theme=None)

# ════════════════════════════════════════════════════════════════════
# VIEW 4 – Side-by-Side Year Comparison
# ════════════════════════════════════════════════════════════════════
elif view == "Side-by-Side Years":
    st.markdown(f'<div class="section">Side-by-Side Year Comparison — {dataset_name}</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    yr_left  = col_l.slider("Year A", int(years[0]), int(years[-1]), 1990)
    yr_right = col_r.slider("Year B", int(years[0]), int(years[-1]), 2020)

    def year_map(yr, mo=6):
        sliced = get_slice(ds, var, yr, mo, _scale)
        df     = slice_to_df(sliced, var)
        # Get shared color range
        vmin = float(df[var].quantile(0.02))
        vmax = float(df[var].quantile(0.98))
        f    = px.scatter_geo(df, lat='lat', lon='lon', color=var,
                              color_continuous_scale='RdBu_r',
                              range_color=[vmin, vmax],
                              projection='natural earth',
                              title=f"{dataset_name} — {yr} (June)",
                              labels={var: unit},
                              hover_data={'lat': ':.1f', 'lon': ':.1f', var: ':.2f'})
        f.update_traces(marker=dict(size=3, opacity=1.0))
        f.update_layout(height=400, paper_bgcolor='#faf9f6',
                        font=dict(family='Georgia', color='#2c2c2c'),
                        margin=dict(l=0, r=0, t=40, b=0),
                        geo=dict(bgcolor='#faf9f6', showocean=True, oceancolor='#c9dff0',
                                 showland=True, landcolor='#e6ddd0',
                                 showcoastlines=True, coastlinecolor='#7a6a56', showframe=False))
        return f

    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(year_map(yr_left),  use_container_width=True, theme=None)
    with col_r:
        st.plotly_chart(year_map(yr_right), use_container_width=True, theme=None)

    # Difference map
    st.markdown('<div class="section">Difference Map (Year B − Year A)</div>', unsafe_allow_html=True)
    left_arr  = get_slice(ds, var, yr_left,  6, _scale)
    right_arr = get_slice(ds, var, yr_right, 6, _scale)
    diff_arr  = right_arr - left_arr
    df_diff   = diff_arr.to_dataframe(name='diff').reset_index().dropna(subset=['diff'])

    fig_diff = px.scatter_geo(df_diff, lat='lat', lon='lon', color='diff',
                               color_continuous_scale='RdBu_r', range_color=[-5, 5],
                               projection='natural earth',
                               title=f"Change: {yr_right} minus {yr_left}  ({unit})",
                               labels={'diff': f'Δ {unit}'},
                               hover_data={'lat': ':.1f', 'lon': ':.1f', 'diff': ':.2f'})
    fig_diff.update_traces(marker=dict(size=3, opacity=1.0))
    fig_diff.update_layout(height=430, paper_bgcolor='#faf9f6',
                            font=dict(family='Georgia', color='#2c2c2c'),
                            geo=dict(bgcolor='#faf9f6', showocean=True, oceancolor='#c9dff0',
                                     showland=True, landcolor='#e6ddd0',
                                     showcoastlines=True, coastlinecolor='#7a6a56', showframe=False))
    st.plotly_chart(fig_diff, use_container_width=True, theme=None)

    # Summary stats
    mean_diff = float(df_diff['diff'].mean())
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Mean change", f"{mean_diff:+.2f} {unit}")
    sc2.metric("Max warming region", f"{df_diff['diff'].max():+.2f} {unit}")
    sc3.metric("Max cooling region", f"{df_diff['diff'].min():+.2f} {unit}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("PyClimaExplorer · Streamlit + Plotly + Xarray · Data: NCEP/NCAR Reanalysis (NOAA PSL)")
