# 🌍 PyClimaExplorer

**PyClimaExplorer** is an interactive, multi-dataset climate dashboard built with Streamlit, Plotly, and Xarray. It allows users to explore global climate data from the NCEP/NCAR Reanalysis dataset (1948–2026) through rich visualizations including heatmaps, time series, dataset comparisons, and side-by-side year analysis.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Dataset Setup](#dataset-setup)
- [Views & Usage](#views--usage)
- [Configuration](#configuration)
- [Notes](#notes)

---

## ✨ Features

- **Global Heatmap** — Visualize monthly climate data on an interactive world map with customizable year and month selection.
- **Time Series** — Plot monthly values at any lat/lon location with a 12-month rolling mean overlay and basic statistics.
- **Dataset Comparison** — Compare all three variables (Temperature, Wind, Precipitation) on a single normalized chart with a correlation matrix.
- **Side-by-Side Years** — Compare two different years visually with a difference map highlighting changes.
- **Dark Sidebar UI** — Clean dark sidebar with white text and Trebuchet MS font for improved readability.
- **Wind Data Filter** — Wind Speed data is automatically filtered to exclude 2026 (pre-2026 only).
- **Temperature in Celsius** — Air Temperature is labeled in °C throughout the interface.

---

## 📁 Project Structure

```
project/
│
├── app.py                  # Main Streamlit application
├── visualization.py        # Reusable Plotly chart functions
├── README.md               # This file
│
└── data/                   # NetCDF data files (not included, see Dataset Setup)
    ├── air.mon.mean.nc     # Air Temperature (NCEP)
    ├── uwnd.mon.mean.nc    # Wind Speed U-component
    └── sample_data.nc      # Precipitation Rate
```

---

## 🛠 Requirements

- Python 3.8+
- streamlit
- xarray
- pandas
- numpy
- plotly
- netCDF4 or scipy (for reading `.nc` files)

---

## ⚙️ Installation

1. **Clone or download** the project folder.

2. **Install dependencies:**

```bash
pip install streamlit xarray pandas numpy plotly netCDF4
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
python -m streamlit run app.py
```

Then open your browser and go to:

```
http://localhost:8501
```

---

## 🗂 Dataset Setup

This app uses **NCEP/NCAR Reanalysis** data from [NOAA PSL](https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html).

Download the following files and place them in a `data/` folder next to `app.py`:

| File               | Variable           | Source               |
| ------------------ | ------------------ | -------------------- |
| `air.mon.mean.nc`  | Air Temperature    | NCEP/NCAR Reanalysis |
| `uwnd.mon.mean.nc` | U-Wind Component   | NCEP/NCAR Reanalysis |
| `sample_data.nc`   | Precipitation Rate | Custom / NCEP        |

> **Note:** The `data/` directory must be in the same folder as `app.py` for the app to load datasets correctly.

---

## 🖥 Views & Usage

### 1. Global Heatmap

- Select a **Dataset**, **Year**, and **Month** from the sidebar.
- The map renders one dot per grid cell colored by value.
- Below the map, an **Annual Global Mean** trend chart and a **Monthly Cycle** bar chart are shown.

### 2. Time Series

- Enter a **Latitude** and **Longitude** to extract data for a specific location.
- Adjust the **Year Range** slider to focus on a period.
- The chart shows raw monthly values and a 12-month rolling mean.
- Summary statistics (Mean, Min, Max) and raw data table are shown below.

### 3. Dataset Comparison

- All three datasets are plotted together as **Z-scores** (normalized) for fair comparison.
- A **Correlation Matrix** heatmap shows relationships between variables.

### 4. Side-by-Side Years

- Choose **Year A** and **Year B** using sliders.
- Both years are displayed side by side (June data).
- A **Difference Map** (Year B − Year A) highlights regional changes.
- Summary statistics show mean, max warming, and max cooling regions.

---

## 🎨 Configuration

Key settings are defined at the top of `app.py`:

```python
DATASETS = {
    "Air Temperature (NCEP)": {"file": "air.mon.mean.nc", "var": "air",   "unit": "C",      "scale": 1.0},
    "Wind Speed U-component": {"file": "uwnd.mon.mean.nc", "var": "uwnd", "unit": "m/s",    "scale": 1.0},
    "Precipitation Rate":     {"file": "sample_data.nc",  "var": "prate", "unit": "mm/day", "scale": 86400.0},
}
```

To add a new dataset, simply add a new entry with the appropriate file, variable name, unit, and scale factor.

---

## 📝 Notes

- Wind Speed data (`uwnd`) is filtered to **exclude 2026** — only pre-2026 data is used in the Global Heatmap view.
- Temperature is labeled as **°C** in the UI (the underlying NCEP data is in Kelvin; relabeling only, no conversion applied).
- The app uses `@st.cache_data` to cache dataset loading for performance.
- All datasets are pre-loaded at startup to avoid repeated disk reads during interaction.

---

## 📄 License

Data sourced from **NCEP/NCAR Reanalysis** provided by NOAA PSL, Boulder, Colorado, USA.

---

_Built By Streamlit · Plotly · Xarray_
